import {NetworkError as BaseNetworkError} from 'components/Fetch';

const NetworkError = ({query}) => <BaseNetworkError reload={query.refetch} />;

export default NetworkError;
