import {Link} from 'react-router-dom';

import DateTime from 'components/DateTime';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');

const ThinktankLink = ({id, label}) => (
    <Link to={`/thinktank/${id}/`}>{label}</Link>
);

const ThinktankRow = ({id, name, publicationCount, scraperCount, lastRun, errorCount, isActive}) => (
    <tr className={isActive || 'disabled'}>
        <td><ThinktankLink id={id} label={name} /></td>
        <td><ThinktankLink id={id} label={publicationCount} /></td>
        <td><ThinktankLink id={id} label={scraperCount} /></td>
        <td>{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td><ThinktankLink id={id} label={errorCount} /></td>
    </tr>
);

export default ThinktankRow;
