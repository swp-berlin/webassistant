import {useQuery} from 'hooks/query';

import Result from './Result';

const Query = ({endpoint, params, ...props}) => {
    const result = useQuery(endpoint, params);

    return (<Result result={result} {...props} />);
};

export default Query;
