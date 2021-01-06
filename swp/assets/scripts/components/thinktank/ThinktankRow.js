import {Link} from 'react-router-dom';

import dateformat from 'utils/dateformat';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');

const ThinktankRow = ({id, name, publicationCount, scraperCount, lastRun, errorCount, isActive}) => (
    <tr className={isActive || 'disabled'}>
        <td><Link to={`thinktank/${id}/`}>{name}</Link></td>
        <td>{publicationCount}</td>
        <td>{scraperCount}</td>
        <td>{isActive ? <time dateTime={lastRun}>{dateformat(lastRun)}</time> || '—' : DisabledLabel}</td>
        <td>{errorCount}</td>
    </tr>
);

export default ThinktankRow;
