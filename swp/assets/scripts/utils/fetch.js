export const CSRFMiddlewareTokenHeaderName = 'X-CSRFToken';

const getBody = data => {
    const body = JSON.stringify(data);
    const contentType = 'application/json';

    return {body, contentType};
};

export const getJSONOptions = (data, CSRFMiddlewareToken, method = 'POST') => {
    const {body, contentType} = getBody(data);

    const headers = {
        [CSRFMiddlewareTokenHeaderName]: CSRFMiddlewareToken,
    };

    if (contentType) {
        headers['Content-Type'] = contentType;
    }

    return {
        method,
        credentials: 'same-origin',
        body,
        headers,
    };
};

export const DefaultResult = {
    success: null,
    status: null,
    result: {
        data: null,
        errors: null,
    },
    error: null,
    response: null,
};

const buildResult = (success, result, response) => {
    const status = response && response.status;

    let data = null;
    let error = null;
    let errors = null;

    if (success) {
        data = result;
    } else if (status) {
        errors = result;
    } else {
        error = result;
    }

    return {success, status, result: {data, errors}, error, response};
};

const DataHandlers = {
    text: response => response.text(),
    json: response => response.json(),
    pdf: response => response.blob(),
};

const getHandler = (response, handlers = DataHandlers) => {
    const contentType = response.headers.get('Content-Type');

    if (contentType === null) throw new Error('Missing content type header.');

    const [mimeType] = contentType.split('; ');
    const [type, subtype] = mimeType.split('/');
    const handler = handlers[mimeType] || handlers[subtype] || handlers[type] || null;

    if (handler === null) throw new Error(`No data handler found for content type ${mimeType}.`);

    return handler;
};

export default async (url, options) => {
    let response = null;

    try {
        response = await fetch(url, options);
    } catch (error) {
        return buildResult(false, error, response);
    }

    if (response.status === 204) return buildResult(true, null, response);

    let handler;

    try {
        handler = getHandler(response);
    } catch (error) {
        return buildResult(false, error, response);
    }

    let result = null;

    try {
        result = await handler(response);
    } catch (error) {
        return buildResult(false, error, response);
    }

    return buildResult(response.ok, result, response);
};

export const download = (blob, filename) => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.setAttribute('download', filename);
    a.click();
    return false;
};
