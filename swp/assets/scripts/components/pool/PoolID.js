import {useParams} from 'react-router-dom';

import {useQuery} from 'hooks/query';


const PoolID = () => {
    const {id, thinktankID} = useParams();
    const {success, result} = useQuery(`thinktank/${thinktankID || id}`, {fields: ['pool']});
    if (success) {
        return (
            <h6>
                {`Pool: ${result.data.pool}`}
            </h6>
        );
    }
    return null;
};

export default PoolID;
