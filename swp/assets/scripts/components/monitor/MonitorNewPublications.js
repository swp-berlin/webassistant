import {useParams} from 'react-router-dom';

import MonitorPreview from './MonitorPreview';


const MonitorNewPublications = () => {
    const {id} = useParams();

    return (
        <MonitorPreview id={+id} onlyNew downloadURL={`/monitor/${id}/publications/new/download/`} />
    );
};

export default MonitorNewPublications;
