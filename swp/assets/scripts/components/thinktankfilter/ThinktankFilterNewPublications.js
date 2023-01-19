import {useParams} from 'react-router-dom';

import ThinktankFilterPreview from './ThinktankFilterPreview';


const ThinktankFilterNewPublications = () => {
    const {monitorID, id} = useParams();

    return (
        <ThinktankFilterPreview monitorID={+monitorID} id={+id} onlyNew />
    );
};

export default ThinktankFilterNewPublications;
