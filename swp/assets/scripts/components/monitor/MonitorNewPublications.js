import MonitorPreview from './MonitorPreview';


const MonitorNewPublications = ({id}) => (
    <MonitorPreview id={+id} onlyNew downloadURL={`/monitor/${id}/publications/new/download/`} />
);

export default MonitorNewPublications;
