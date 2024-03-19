/* eslint-disable max-classes-per-file */

import * as Message from 'swp/messages';

export const CSRFMiddlewareTokenHeaderName = 'X-CSRFToken';

export class NetworkError extends Error {}

export class DecodeError extends Error {

    constructor(response, error) {
        super(error);
        this.response = response;
    }

}

export class HttpError extends Error {

    constructor(response, data) {
        super(response.statusText);
        this.code = response.status;
        this.response = response;
        this.data = data;
    }

}

const DataHandlers = {
    text: response => response.text(),
    json: response => response.json(),
    pdf: response => response.blob(),
};

export const getHandler = (response, handlers = DataHandlers) => {
    const contentType = response.headers.get('Content-Type');

    if (!contentType) throw new DecodeError(response, 'Missing content type header.');

    const [mimeType] = contentType.split('; ');
    const [type, subtype] = mimeType.split('/');
    const handler = handlers[mimeType] || handlers[subtype] || handlers[type];

    if (!handler) throw new DecodeError(response, `No data handler found for content type ${mimeType}.`);

    return handler;
};

export const getErrorStatusCode = error => {
    if (error instanceof HttpError) return error.code;
    if (error instanceof DecodeError) return error.response.status;

    return null;
};

export const isNotFound = error => getErrorStatusCode(error) === 404;
export const isBadRequest = error => getErrorStatusCode(error) === 400;

const DefaultClientErrors = {};

export const getClientErrors = error => (
    (error instanceof HttpError && error.code === 400) ? error.data : DefaultClientErrors
);

export const getErrorMessage = error => {
    if (error instanceof NetworkError) return Message.NetworkError;

    if (error instanceof HttpError) {
        switch (error.code) {
            case 500:
                return Message.ServerError;
            case 502:
            case 503:
                return Message.Maintenance;
            default:
                if (error.code in Message.HttpErrorMessages) return Message.HttpErrorMessages[error.code];

                return Message.getGenericErrorMessage(error.response.statusText);
        }
    }

    return Message.getGenericErrorMessage(error);
};

const getBody = data => {
    if (data instanceof FormData) return {body: data};

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

export default async (url, options) => {
    const request = fetch(url, options);

    let response;

    try {
        response = await request;
    } catch (error) {
        throw new NetworkError(error);
    }

    if (response.status === 204) return null;

    const handler = getHandler(response);

    let data;

    try {
        data = await handler(response);
    } catch (error) {
        throw new DecodeError(response, error);
    }

    if (response.ok) return data;

    throw new HttpError(response, data);
};
