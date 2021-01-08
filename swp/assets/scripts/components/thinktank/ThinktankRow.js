import {Link} from 'react-router-dom';

import DateTime from 'components/DateTime';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');

const ThinktankRow = ({id, name, publicationCount, scraperCount, lastRun, errorCount, isActive}) => (
    <tr className={isActive || 'disabled'}>
        <td><Link to={`thinktank/${id}/`}>{name}</Link></td>
        <td>{publicationCount}</td>
        <td>{scraperCount}</td>
        <td>{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td>{errorCount}</td>
    </tr>
);

export default ThinktankRow;
