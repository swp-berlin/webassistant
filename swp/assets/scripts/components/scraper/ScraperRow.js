import {Link} from 'react-router-dom';

import _ from 'utils/i18n';

import DateTime from 'components/DateTime';

import ScraperStartButtons from './ScraperStartButtons';
import ScraperCloneDialogButton from './ScraperCloneDialogButton';

const DisabledLabel = _('disabled');

const ScraperLink = ({id, thinktankID, children, ...props}) => (
    <Link to={`/thinktank/${thinktankID}/scraper/${id}/`} {...props}>
        {children}
    </Link>
);

const ExternalLink = ({url}) => <a href={url} target="_blank" rel="noreferrer">{url}</a>;

const ScraperRow = ({id, thinktankID, url, type, categories, lastRun, errorCount, isActive, isRunning, canManage}) => (
    <tr className={isActive ? null : 'disabled'} data-id={id}>
        <td>
            {canManage
                ? <ScraperLink id={id} thinktankID={thinktankID}>{url}</ScraperLink>
                : <ExternalLink url={url} />}
        </td>
        <td>{type}</td>
        <td>{categories}</td>
        <td>{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td className="text-right">{errorCount}</td>
        <td>
            <ScraperStartButtons id={id} thinktankID={thinktankID} isRunning={isRunning} />
            <ScraperCloneDialogButton thinktankID={thinktankID} scraperID={id} />
        </td>
    </tr>
);

export default ScraperRow;
