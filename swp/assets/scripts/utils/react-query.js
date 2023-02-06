import {QueryClient} from 'react-query';

import {buildAPIURL} from './api';
import fetch, {NetworkError} from './react-query-fetch';
import {Slash, withParams} from './url';

const isURL = value => value.indexOf(Slash) >= 0;

const getURL = queryKey => {
    const lastIndex = queryKey.length - 1;
    const lastPart = queryKey[lastIndex];
    const [firstPart] = queryKey;

    let parts = queryKey;
    let params = null;

    if (typeof lastPart === 'object') {
        parts = queryKey.slice(0, lastIndex);
        params = lastPart;
    }

    let baseURL;

    if (parts.length === 1 && isURL(firstPart)) {
        baseURL = firstPart;
    } else {
        baseURL = buildAPIURL(...parts);
    }

    return params ? withParams(baseURL, params) : baseURL;
};

export const buildRequest = (url, options = {}) => {
    const controller = new AbortController();
    const request = fetch(url, {
        credentials: 'same-origin',
        signal: controller.signal,
        ...options,
    });

    request.cancel = () => controller.abort();

    return request;
};

export const defaultQueryFn = ({queryKey, pageParam}) => buildRequest(pageParam || getURL(queryKey));

export const defaultRetry = (failureCount, error) => error instanceof NetworkError && failureCount < 5;

export default new QueryClient({
    defaultOptions: {
        queries: {
            retry: defaultRetry,
            queryFn: defaultQueryFn,
        },
    },
});
