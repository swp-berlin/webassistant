import {useParams} from 'react-router-dom';

import ThinktankFilterPreview from './ThinktankFilterPreview';


const ThinktankFilterPublications = () => {
    const {monitorID, id} = useParams();

    return (
        <ThinktankFilterPreview monitorID={+monitorID} id={+id} />
    );
};

export default ThinktankFilterPublications;
