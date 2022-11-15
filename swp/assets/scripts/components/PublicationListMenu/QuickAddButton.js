import {useCallback} from 'react';
import {Button} from '@blueprintjs/core';

import _, {interpolate} from 'utils/i18n';

import {useToggleMutation} from './hooks';

const AddLabel = _('Add to %(name)s');
const RemoveLabel = _('Remove from %(name)s');

const QuickAddButton = ({publicationID, publicationLists}) => {
    const [lastUpdatedPublicationList] = publicationLists;
    const {id: publicationListID, publication_list: publications} = lastUpdatedPublicationList;
    const isIncluded = publications.includes(publicationID);
    const {mutate, isLoading} = useToggleMutation(publicationListID, publicationID, isIncluded);
    const title = interpolate(isIncluded ? RemoveLabel : AddLabel, lastUpdatedPublicationList);
    const handleClick = useCallback(
        event => {
            event.preventDefault();
            mutate();
        },
        [mutate],
    );

    return (
        <Button
            title={title}
            icon={isIncluded ? 'remove' : 'add'}
            loading={isLoading}
            onClick={handleClick}
        />
    );
};

export default QuickAddButton;
