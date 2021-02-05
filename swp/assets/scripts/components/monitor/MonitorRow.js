import {Link} from 'react-router-dom';


const MonitorLink = ({id, children, ...props}) => (
    <Link to={`/monitor/${id}/`} {...props}>
        {children}
    </Link>
);

const ThinktankRow = ({id, name, recipientCount, publicationCount, newPublicationCount}) => (
    <tr>
        <td><MonitorLink id={id}>{name}</MonitorLink></td>
        <td className="text-right">{recipientCount}</td>
        <td className="text-right">{publicationCount}</td>
        <td className="text-right">{newPublicationCount}</td>
    </tr>
);

export default ThinktankRow;
