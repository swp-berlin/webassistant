import BaseClientError from 'components/Fetch/ClientError';

const ClientError = ({error}) => <BaseClientError status={error.code} />;

export default ClientError;
