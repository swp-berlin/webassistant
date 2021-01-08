import {Link} from 'react-router-dom';

import DateTime from 'components/DateTime';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');

const ScraperRow = ({id, url, type, lastRun, errorCount, isActive}) => (
    <tr className={isActive ? null : 'disabled'} data-id={id}>
        <td><Link to={url}>{url}</Link></td>
        <td>{type}</td>
        <td>{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td>{errorCount}</td>
    </tr>
);

export default ScraperRow;
