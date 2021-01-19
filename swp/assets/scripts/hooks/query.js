import {useCallback, useEffect, useRef, useState} from 'react';

import {buildAPIURL} from 'utils/api';
import {CSRFMiddlewareToken} from 'utils/csrf';
import getResult, {DefaultResult, getJSONOptions} from 'utils/fetch';
import {withParams} from 'utils/url';


export const useFetch = url => {
    const [loading, setLoading] = useState(false);
    const resultRef = useRef({...DefaultResult, request: null, called: false});

    const setResult = (loading, result) => {
        if (loading || result.request === resultRef.current.request) {
            resultRef.current = result;
            setLoading(loading);
        }
    };

    const fetch = useCallback(
        async options => {
            const request = getResult(url, options);

            setResult(true, {...DefaultResult, request, called: true});

            const {response, ...result} = await request;

            setResult(false, {...result, request, response, called: true});

            return resultRef.current;
        },
        [url],
    );

    useEffect(() => { resultRef.current.request = null; }, [resultRef]);

    return [fetch, {...resultRef.current, loading}];
};

export const useAPIFetch = (endpoint, params) => {
    let url = buildAPIURL(endpoint);

    if (params) url = withParams(url, params);

    return useFetch(url);
};

export const useLazyQuery = (endpoint, params) => {
    const [fetch, result] = useAPIFetch(endpoint, params);
    const loading = result.called ? result.loading : true;

    return {...result, loading, fetch};
};

export const useQuery = (endpoint, params) => {
    const result = useLazyQuery(endpoint, params);
    const {fetch} = result;

    useEffect(() => { fetch(); }, [fetch]);

    return result;
};

export const useMutation = (endpoint, params) => {
    const [fetch, result] = useAPIFetch(endpoint, params);

    const mutate = useCallback(
        (data, method = 'POST') => {
            const options = getJSONOptions(data, CSRFMiddlewareToken, method);

            return fetch(options);
        },
        [fetch],
    );

    return [mutate, result];
};
