import {Link} from 'react-router-dom';

import DateTime from 'components/DateTime';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');

const ScraperLink = ({id, children, ...props}) => (
    <Link to={`/scraper/${id}/`} {...props}>
        {children}
    </Link>
);

const ScraperRow = ({id, url, type, lastRun, errorCount, isActive}) => (
    <tr className={isActive ? null : 'disabled'} data-id={id}>
        <td><ScraperLink id={id}>{url}</ScraperLink></td>
        <td>{type}</td>
        <td>{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td className="text-right">{errorCount}</td>
    </tr>
);

export default ScraperRow;
