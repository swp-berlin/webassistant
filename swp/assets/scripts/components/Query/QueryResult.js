import {cloneElement, isValidElement} from 'react';

import {HttpError, NetworkError, DecodeError} from 'utils/react-query-fetch';

import LoadingComponent from './Loading';
import GenericErrorComponent from './GenericError';
import NetworkErrorComponent from './NetworkError';
import ClientErrorComponent from './ClientError';
import ServerErrorComponent from './ServerError';

export const DefaultComponents = {
    idle: LoadingComponent,
    loading: LoadingComponent,
    generic: GenericErrorComponent,
    network: NetworkErrorComponent,
    401: ClientErrorComponent,
    403: ClientErrorComponent,
    404: ClientErrorComponent,
    500: ServerErrorComponent,
    502: ServerErrorComponent,
    503: ServerErrorComponent,
};

const renderErrorComponent = (error, query, components) => {
    let Child = null;

    if (error instanceof DecodeError) Child = components.generic;
    else if (error instanceof NetworkError) Child = components.network;
    else if (error instanceof HttpError) Child = components[error.code] || components.generic;

    return Child && <Child error={error} query={query} />;
};

export const renderChild = (children, data, ...args) => (
    isValidElement(children) ? cloneElement(children, data) : children(data, ...args)
);

const QueryResult = ({query, components = {}, showErrors = true, children}) => {
    const {isLoading, isIdle, isError, data, error} = query;
    const {loading: Loading, idle: Idle, ...errorComponents} = {...DefaultComponents, ...components};

    if (isIdle) return Idle && <Idle query={query} />;
    if (isLoading) return Loading && <Loading query={query} />;
    if (isError) return showErrors && renderErrorComponent(error, query, errorComponents);

    return renderChild(children, data, query);
};

export default QueryResult;
