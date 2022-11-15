import {Link} from 'react-router-dom';
import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';

import PublicationListMenuItem from './PublicationListMenuItem';

const ButtonTitle = _('Close');
const LinkTitle = _('Manage publication lists…');

const PublicationListDialog = ({publicationID, publicationLists, onClose}) => (
    <div className="absolute right-0 top-0 bg-white border-black p-1">
        <Button title={ButtonTitle} icon="cross" onClick={onClose} />
        <ul className="list-none p-0">
            {publicationLists.map(publicationList => (
                <PublicationListMenuItem
                    key={publicationList.id}
                    publicationID={publicationID}
                    {...publicationList}
                />
            ))}
            <li className="whitespace-nowrap">
                <Link to="/publication-list/">
                    {LinkTitle}
                </Link>
            </li>
        </ul>
    </div>
);

export default PublicationListDialog;
