import {useParams} from 'react-router-dom';

import MonitorPreview from './MonitorPreview';


const MonitorPublications = () => {
    const {id} = useParams();

    return (
        <MonitorPreview id={+id} downloadURL={`/monitor/${id}/publications/download/`} />
    );
};

export default MonitorPublications;
