import {ChoicesQuery} from 'components/Fetch';
import {Endpoint, getParams} from 'components/PoolQuery';

const prepareChoice = ({id, name}) => ({value: id, label: name});

const PoolChoicesQuery = ({canManage = false, children, ...props}) => {
    const params = getParams(canManage);

    return (
        <ChoicesQuery endpoint={Endpoint} params={params} prepareChoice={prepareChoice} {...props}>
            {children}
        </ChoicesQuery>
    );
};

export default PoolChoicesQuery;
