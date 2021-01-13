import DateTime from 'components/DateTime';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');

const ScraperRow = ({id, url, type, lastRun, errorCount, isActive}) => (
    <tr className={isActive ? null : 'disabled'} data-id={id}>
        <td><a href={url}>{url}</a></td>
        <td>{type}</td>
        <td>{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td className="text-right">{errorCount}</td>
    </tr>
);

export default ScraperRow;
