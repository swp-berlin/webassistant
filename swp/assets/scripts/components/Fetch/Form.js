import {useCallback, useMemo} from 'react';
import {useForm} from 'react-hook-form';
import {useHistory} from 'react-router-dom';

import _, {interpolate} from 'utils/i18n';
import {setErrors} from 'utils/form';
import Toaster from 'utils/toaster';

import {useMutation} from 'hooks/query';

import getToast from './Result';
import {DefaultProps as NetworkErrorProps} from './NetworkError';
import {Fallback as ClientErrorFallback} from './ClientError';
import {Fallback as ServerErrorFallback} from './ServerError';

const DefaultSuccessMessage = _('Your data has been saved successfully.');
const DefaultNetworkErrorMessage = NetworkErrorProps.description;
const DefaultClientErrorMessage = ClientErrorFallback.description;
const DefaultServerErrorMessage = ServerErrorFallback.description;
const DefaultMaintenanceMessage = _('We are currently doing maintenance work. Please try again in a few seconds.');
const DefaultHttpErrorMessages = {
    400: _('Please correct the errors below.'),
    401: _('You have to be logged in to make this request.'),
    403: _('You are not allowed to make this request.'),
    404: _('The data you wanted to change does not exist anymore.'),
    502: DefaultMaintenanceMessage,
    503: DefaultMaintenanceMessage,
};

const handleSuccess = (data, result, {successMessage}) => ({
    intent: 'success',
    message: interpolate(successMessage, data),
});

const handleNetworkError = (error, resubmit, {networkErrorMessage}) => ({
    intent: 'warning',
    message: interpolate(networkErrorMessage, {error}),
});

const handleHttpError = (status, errors, {setErrors, httpErrorMessages}, fallbackMessage) => {
    const message = httpErrorMessages[status] || DefaultHttpErrorMessages[status] || fallbackMessage;

    if (status === 400 && setErrors) setErrors(errors);

    return {
        intent: 'danger',
        message,
    };
};

const handleClientError = (status, errors, resubmit, props) => (
    handleHttpError(status, errors, props, DefaultClientErrorMessage)
);

const handleServerError = (status, errors, resubmit, props) => (
    handleHttpError(status, errors, props, DefaultServerErrorMessage)
);

const DefaultHandlers = {
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
        const {history} = options;
        const redirectURL = getRedirectURL(result, options);

        if (history && redirectURL) history.push(redirectURL);
    }

    return result;
};

export const useMutationResult = (endpoint, {params, ...options}, dependencies) => {
    const history = useHistory();
    const [mutate, result] = useMutation(endpoint, params);

    const handleSubmit = useCallback(
        async (data, method) => handleMutationResult(
            await mutate(data, method),
            {history, ...options},
        ),
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [mutate, history, ...dependencies],
    );

    return [handleSubmit, result];
};

export const useMutationForm = (endpoint, formOptions, mutationOptions, mutationDependencies) => {
    const form = useForm({criteriaMode: 'all', ...formOptions});
    const {setError, handleSubmit} = form;
    const {method, ...options} = {setErrors: errors => setErrors(setError, errors), method: 'POST', ...mutationOptions};
    const [mutate, result] = useMutationResult(endpoint, options, [setError, ...mutationDependencies]);
    const onSubmit = useMemo(() => handleSubmit(values => mutate(values, method)), [handleSubmit, mutate, method]);

    return [onSubmit, form, result];
};

const Form = ({children, endpoint, ...options}) => {
    const [handleSubmit, result] = useMutationResult(endpoint, options);

    return children(handleSubmit, result);
};

export default Form;
