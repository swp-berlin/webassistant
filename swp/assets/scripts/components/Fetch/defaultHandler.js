import {cloneElement, isValidElement} from 'react';

import Loading from './Loading';
import NetworkError from './NetworkError';
import ClientError from './ClientError';
import ServerError from './ServerError';

const handleLoading = (called, {loadingProps}) => (
    called && <Loading {...loadingProps} />
);

const handleSuccess = (data, result, {children, ...props}) => (
    isValidElement(children)
        ? cloneElement(children, {result, ...data})
        : children(data, result, props)
);

const handleNetworkError = (error, reload, {networkErrorProps}) => (
    <NetworkError {...networkErrorProps} reload={reload} />
);

const handleClientError = (status, errors, reload, {clientErrorProps}) => (
    <ClientError {...clientErrorProps} status={status} />
);

const handleServerError = (status, errors, reload, {serverErrorProps}) => (
    <ServerError {...serverErrorProps} status={status} reload={reload} />
);

export {
    handleLoading,
    handleSuccess,
    handleNetworkError,
    handleClientError,
    handleServerError,
};

export default {
    handleLoading,
    handleSuccess,
    handleNetworkError,
    handleClientError,
    handleServerError,
};
