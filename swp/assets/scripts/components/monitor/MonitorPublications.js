import MonitorPreview from './MonitorPreview';


const MonitorPublications = ({id}) => (
    <MonitorPreview id={+id} downloadURL={`/monitor/${id}/publications/download/`} />
);

export default MonitorPublications;
