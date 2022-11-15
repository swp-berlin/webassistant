import {useMutation as useBaseMutation} from 'react-query';
import {Intent} from '@blueprintjs/core';

import Toaster from 'utils/toaster';
import {CSRFMiddlewareToken} from 'utils/csrf';
import getResult, {getJSONOptions, getErrorMessage} from 'utils/react-query-fetch';

export const useMutation = (url, method, mutationOptions) => {
    const {onError, ...options} = mutationOptions || {};
    const mutationFn = data => getResult(url, getJSONOptions(data, CSRFMiddlewareToken, method));

    return useBaseMutation([url, method], mutationFn, {
        ...options,
        onError(error, ...args) {
            const message = onError && onError(error, ...args);

            if (message === false) return;

            Toaster.show({message: message || getErrorMessage(error), intent: Intent.WARNING});
        },
    });
};
