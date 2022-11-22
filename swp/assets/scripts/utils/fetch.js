import {getHandler, getJSONOptions} from './react-query-fetch';

export {getJSONOptions};

export const DefaultResult = {
    success: null,
    status: null, // HTTP Status code
    result: {
        data: null, // Result if `status` ~ 200
        errors: null, // .. or otherwise
    },
    error: null, // Network error
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
