import {Link} from 'react-router-dom';
import {Tag} from '@blueprintjs/core';

import _, {interpolate} from 'utils/i18n';

const Label = _('%(name)s (%(count)s publications)');
const DefaultLabel = _('Default');

const PublicationListEntry = ({id, name, entry_count: count, isDefault}) => (
    <li className="publication-list-entry">
        <Link to={`${id}/`}>
            {interpolate(Label, {name, count})}
        </Link>
        {isDefault && <Tag className="ml-1">{DefaultLabel}</Tag>}
    </li>
);

export default PublicationListEntry;
