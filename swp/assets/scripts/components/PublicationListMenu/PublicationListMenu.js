import {Children, cloneElement} from 'react';
import {ButtonGroup} from '@blueprintjs/core';

import {useLastUpdatedPublicationList} from './hooks';

const NotButtonGroup = ({children}) => children;

const PublicationListMenu = ({publication, publicationLists, children}) => {
    const lastUpdatedPublicationList = useLastUpdatedPublicationList(publicationLists);
    const props = {publication, publicationLists, lastUpdatedPublicationList};
    const Group = Children.count(children) > 1 ? ButtonGroup : NotButtonGroup;

    return (
        <aside className="absolute right-0 top-0">
            <Group vertical>
                {Children.map(children, child => cloneElement(child, props))}
            </Group>
        </aside>
    );
};

export default PublicationListMenu;
