import {Link} from 'react-router-dom';

import _, {interpolate} from 'utils/i18n';

import DefaultTag from 'components/DefaultTag';

const Label = _('%(name)s (%(count)s publications)');

const PublicationListEntry = ({id, name, entry_count: count, isDefault}) => (
    <li className="publication-list-entry">
        <Link to={`${id}/`}>
            {interpolate(Label, {name, count})}
        </Link>
        {isDefault && <DefaultTag />}
    </li>
);

export default PublicationListEntry;
