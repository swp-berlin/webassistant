import defaultHandler from './defaultHandler';

const Result = ({query: q, result, ...handler}) => {
    const query = q || result;
    const {handleLoading, handleSuccess, handleNetworkError, handleClientError, handleServerError, ...props} = handler;
    const {called, loading, success, status, result: {data, errors}, error, fetch: reload} = query;

    if (called === false || loading) return handleLoading(called, props);
    if (success) return handleSuccess(data, query, props);
    if (status === null) return handleNetworkError(error, reload, props);

    return (status >= 400 && status < 500 ? handleClientError : handleServerError)(status, errors, reload, props);
};

Result.defaultProps = {
    ...defaultHandler,
};

export default Result;
