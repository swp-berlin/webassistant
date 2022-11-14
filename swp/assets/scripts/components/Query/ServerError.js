import BaseServerError from 'components/Fetch/ServerError';

const ServerError = ({error, query}) => <BaseServerError status={error.code} reload={query.refetch} />;

export default ServerError;
