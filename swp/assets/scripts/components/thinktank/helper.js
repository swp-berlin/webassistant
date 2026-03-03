import {useParams} from 'react-router-dom';

import {useQuery} from 'hooks/query';

import _, {interpolate} from 'utils/i18n';


const ThinktankLabel = _('Thinktank %s');

export const getThinktankLabel = (id, {result: {data}, loading}) => (
    loading || !data ? interpolate(ThinktankLabel, [id], false) : data.name
);

export const PoolID = () => {
    const {id, thinktankID} = useParams();
    const {success, result} = useQuery(`thinktank/${thinktankID || id}`, {fields: ['pool']});
    if (success) {
        return <h6> Pool: {result.data.pool} </h6>;
    }
    return null;
}
