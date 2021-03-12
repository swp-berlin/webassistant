import {Link} from 'react-router-dom';

import DateTime from 'components/DateTime';
import _ from 'utils/i18n';

const DisabledLabel = _('disabled');

const MonitorLink = ({id, children, ...props}) => (
    <Link to={`/monitor/${id}/`} {...props}>
        {children}
    </Link>
);

const ThinktankRow = ({id, name, recipientCount, publicationCount, newPublicationCount, lastSent, isActive}) => (
    <tr className={isActive ? '' : 'disabled'}>
        <td><MonitorLink id={id}>{name}</MonitorLink></td>
        <td className="text-right">{recipientCount}</td>
        <td className="text-right">{publicationCount}</td>
        <td className="text-right">{newPublicationCount}</td>
        <td className="text-right">{isActive ? <DateTime value={lastSent} /> : DisabledLabel}</td>
    </tr>
);

export default ThinktankRow;
