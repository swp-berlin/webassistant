import Query from 'components/Query';

export const Endpoint = 'pool';

export const getParams = canManage => canManage ? {can_manage: canManage} : null;

const PoolQuery = ({canManage = false, children, ...props}) => {
    const params = getParams(canManage);
    const queryKey = [Endpoint, params];

    return (
        <Query queryKey={queryKey} {...props}>
            {children}
        </Query>
    );
};

export default PoolQuery;
