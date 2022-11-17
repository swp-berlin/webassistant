import {UL} from '@blueprintjs/core';

import PublicationListEntry from './PublicationListEntry';

const PublicationList = ({publicationLists}) => (
    <UL className="publication-list list-none p-0 mt-4">
        {publicationLists.map((publicationList, index) => (
            <PublicationListEntry
                key={publicationList.id}
                {...publicationList}
                isDefault={index === 0}
            />
        ))}
    </UL>
);

export default PublicationList;
