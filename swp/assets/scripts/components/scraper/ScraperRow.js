import DateTime from 'components/DateTime';
import ExternalLink from 'components/Navigation/ExternalLink';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');

const ScraperRow = ({id, url, type, lastRun, errorCount, isActive}) => (
    <tr className={isActive ? null : 'disabled'} data-id={id}>
        <td><ExternalLink to={url} /></td>
        <td>{type}</td>
        <td>{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td className="text-right">{errorCount}</td>
    </tr>
);

export default ScraperRow;
