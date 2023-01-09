import {UL} from '@blueprintjs/core';

import {useLastUpdatedPublicationList} from 'components/PublicationListMenu';

import PublicationListEntry from './PublicationListEntry';

const PublicationList = ({publicationLists, lastUpdatedPublicationList}) => (
    <UL className="publication-list list-none p-0 mt-4">
        {publicationLists.map(publicationList => (
            <PublicationListEntry
                key={publicationList.id}
                {...publicationList}
                isDefault={publicationList === lastUpdatedPublicationList}
            />
        ))}
    </UL>
);

const PublicationListController = ({publicationLists}) => {
    const lastUpdatedPublicationList = useLastUpdatedPublicationList(publicationLists);

    return (
        <PublicationList
            publicationLists={publicationLists}
            lastUpdatedPublicationList={lastUpdatedPublicationList}
        />
    );
};

export default PublicationListController;
