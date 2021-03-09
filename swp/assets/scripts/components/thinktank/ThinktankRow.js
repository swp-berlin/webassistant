import {Link} from 'react-router-dom';

import DateTime from 'components/DateTime';
import _ from 'utils/i18n';


const DisabledLabel = _('disabled');
const ActiveTotalLabel = _('active / total');

const ThinktankLink = ({id, children, ...props}) => (
    <Link to={`/thinktank/${id}/`} {...props}>
        {children}
    </Link>
);

const PublicationsLink = ({id, children}) => (
    <Link to={`/thinktank/${id}/publications/`}>
        {children}
    </Link>
);

const ThinktankRow = ({
    id, name, publicationCount, scraperCount, activeScraperCount, lastRun, errorCount, isActive,
}) => (
    <tr className={isActive ? '' : 'disabled'}>
        <td><ThinktankLink id={id}>{name}</ThinktankLink></td>
        <td className="text-right"><PublicationsLink id={id}>{publicationCount}</PublicationsLink></td>
        <td className="text-right" title={ActiveTotalLabel}>
            <ThinktankLink id={id}>
                {`${activeScraperCount} / ${scraperCount}`}
            </ThinktankLink>
        </td>
        <td className="text-right">{isActive ? <DateTime value={lastRun} /> : DisabledLabel}</td>
        <td className="text-right"><ThinktankLink id={id}>{errorCount}</ThinktankLink></td>
    </tr>
);

export default ThinktankRow;
