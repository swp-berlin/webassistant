import {useCallback, useMemo} from 'react';
import {useForm} from 'react-hook-form';
import {useNavigate} from 'react-router-dom';
import {Intent} from '@blueprintjs/core';

import _, {interpolate} from 'utils/i18n';
import {setErrors} from 'utils/form';
import Toaster from 'utils/toaster';

import {HttpErrorMessages} from 'swp/messages';

import {useMutation} from 'hooks/query';

import getToast from './Result';
import {DefaultProps as NetworkErrorProps} from './NetworkError';
import {Fallback as ClientErrorFallback} from './ClientError';
import {Fallback as ServerErrorFallback} from './ServerError';

const DefaultSuccessMessage = _('Your data has been saved successfully.');
const DefaultNetworkErrorMessage = NetworkErrorProps.description;
const DefaultClientErrorMessage = ClientErrorFallback.description;
const DefaultServerErrorMessage = ServerErrorFallback.description;
const DefaultHttpErrorMessages = HttpErrorMessages;

const handleSuccess = (data, result, {successMessage}) => ({
    intent: Intent.SUCCESS,
    message: interpolate(successMessage, data),
});

const handleNetworkError = (error, resubmit, {networkErrorMessage}) => ({
    intent: Intent.WARNING,
    message: interpolate(networkErrorMessage, {error}),
});

const handleHttpError = (status, errors, {setErrors, httpErrorMessages}, fallbackMessage) => {
    const message = httpErrorMessages[status] || DefaultHttpErrorMessages[status] || fallbackMessage;

    if (status === 400 && setErrors) setErrors(errors);

    return {
        intent: Intent.DANGER,
        message,
    };
};

const handleClientError = (status, errors, resubmit, props) => (
    handleHttpError(status, errors, props, DefaultClientErrorMessage)
);

const handleServerError = (status, errors, resubmit, props) => (
    handleHttpError(status, errors, props, DefaultServerErrorMessage)
);

export const DefaultHandlers = {
    handleSuccess,
    handleNetworkError,
    handleClientError,
    handleServerError,
};

const DefaultMessages = {
    successMessage: DefaultSuccessMessage,
    networkErrorMessage: DefaultNetworkErrorMessage,
    httpErrorMessages: DefaultHttpErrorMessages,
};

const getRedirectURL = ({result}, {redirectURL}) => (
    typeof redirectURL === 'function' ? redirectURL(result.data) : redirectURL
);

export const handleMutationResult = (result, options) => {
    const toast = getToast({result, ...DefaultHandlers, ...DefaultMessages, ...options});

    if (toast) Toaster.show(toast);

    if (result.success) {
        const {navigate} = options;
        const redirectURL = getRedirectURL(result, options);

        if (navigate && redirectURL) navigate(redirectURL);
    }

    return result;
};

export const useMutationResult = (endpoint, {params, ...options}, dependencies) => {
    const navigate = useNavigate();
    const [mutate, result] = useMutation(endpoint, params);

    const handleSubmit = useCallback(
        async (data, method) => handleMutationResult(
            await mutate(data, method),
            {navigate, ...options},
        ),
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [mutate, navigate, ...dependencies],
    );

    return [handleSubmit, result];
};

export const useMutationForm = (endpoint, formOptions, mutationOptions, mutationDependencies) => {
    const form = useForm({criteriaMode: 'all', ...formOptions});
    const {setError, handleSubmit} = form;
    const {method, ...options} = {setErrors: errors => setErrors(setError, errors), method: 'POST', ...mutationOptions};
    const [mutate, result] = useMutationResult(endpoint, options, [setError, ...mutationDependencies]);
    const onSubmit = useMemo(() => handleSubmit(values => mutate(values, method)), [handleSubmit, mutate, method]);

    return [onSubmit, form, result, mutate];
};

const Form = ({children, endpoint, ...options}) => {
    const [handleSubmit, result] = useMutationResult(endpoint, options);

    return children(handleSubmit, result);
};

export default Form;
