import {Link} from 'react-router-dom';

import _, {interpolate} from 'utils/i18n';

const Label = _('%(name)s (%(count)s publications)');

const PublicationListEntry = ({id, name, entry_count: count}) => (
    <li className="publication-list-entry">
        <Link to={`${id}/`}>
            {interpolate(Label, {name, count})}
        </Link>
    </li>
);

export default PublicationListEntry;
