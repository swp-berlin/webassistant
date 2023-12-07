import Query from 'components/Query';

import QueryError from './QueryError';

const QueryComponents = {
    400: QueryError,
};

const SearchQuery = ({query, pools, startDate, endDate, page, children}) => {
    const params = {query};

    if (pools.length) params.pool = pools;
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    if (page) params.page = page;

    return (
        <Query queryKey={['publication', 'research', params]} components={QueryComponents}>
            {children}
        </Query>
    );
};

export default SearchQuery;
