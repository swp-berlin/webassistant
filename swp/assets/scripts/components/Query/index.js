import {useQuery} from 'react-query';

import QueryResult from './QueryResult';

export {QueryResult};

const Query = ({queryKey, children, ...options}) => {
    const query = useQuery(queryKey, options);

    return (
        <QueryResult {...options} query={query}>
            {children}
        </QueryResult>
    );
};

export default Query;
