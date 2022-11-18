import {Link} from 'react-router-dom';
import {Popover} from '@blueprintjs/core';

import _ from 'utils/i18n';

import PublicationListMenuItem from './PublicationListMenuItem';

const LinkTitle = _('Manage publication lists…');

const PublicationListDialog = ({publication, publicationLists, children, ...popoverProps}) => (
    <Popover {...popoverProps} placement="left-start">
        {children}
        <div className="content p-4">
            <ul className="list-none p-0 m-0">
                {publicationLists.map(publicationList => (
                    <PublicationListMenuItem
                        key={publicationList.id}
                        publicationID={publication.id}
                        {...publicationList}
                    />
                ))}
                <li className="whitespace-nowrap mt-3">
                    <Link to="/publication-list/">
                        {LinkTitle}
                    </Link>
                </li>
            </ul>
        </div>
    </Popover>
);

export default PublicationListDialog;
