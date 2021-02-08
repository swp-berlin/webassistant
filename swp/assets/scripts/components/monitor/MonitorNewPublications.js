import MonitorPreview from './MonitorPreview';


const MonitorNewPublications = ({id}) => (
    <MonitorPreview id={+id} onlyNew />
);

export default MonitorNewPublications;
