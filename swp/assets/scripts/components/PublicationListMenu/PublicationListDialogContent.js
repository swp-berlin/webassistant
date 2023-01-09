import {Link} from 'react-router-dom';

import _ from 'utils/i18n';

import PublicationListDialogItem from './PublicationListDialogItem';

const LinkTitle = _('Manage publication lists…');

const PublicationListDialogContent = ({publication, publicationLists, lastUpdatedPublicationList}) => (
    <div className="content p-4">
        <ul className="list-none p-0 m-0">
            {publicationLists.map(publicationList => (
                <PublicationListDialogItem
                    key={publicationList.id}
                    publicationID={publication.id}
                    isLastUpdated={publicationList === lastUpdatedPublicationList}
                    {...publicationList}
                />
            ))}
            <li className="whitespace-nowrap mt-3">
                <Link to="/search/publication-list/">
                    {LinkTitle}
                </Link>
            </li>
        </ul>
    </div>
);

export default PublicationListDialogContent;
