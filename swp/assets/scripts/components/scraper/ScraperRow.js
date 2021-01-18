import {Link} from 'react-router-dom';

import DateTime from 'components/DateTime';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');

const ScraperLink = ({id, thinktankID, children, ...props}) => (
    <Link to={`/thinktank/${thinktankID}/scraper/${id}/`} {...props}>
        {children}
    </Link>
);

const ScraperRow = ({id, thinktankID, url, type, lastRun, errorCount, isActive}) => (
    <tr className={isActive ? null : 'disabled'} data-id={id}>
        <td><ScraperLink id={id} thinktankID={thinktankID}>{url}</ScraperLink></td>
        <td>{type}</td>
        <td>{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td className="text-right">{errorCount}</td>
    </tr>
);

export default ScraperRow;
