import {useCallback} from 'react';
import {Button} from '@blueprintjs/core';

import _, {interpolate} from 'utils/i18n';

import {useToggleMutation} from './hooks';

const AddLabel = _('Add to %(name)s');
const RemoveLabel = _('Remove from %(name)s');

const QuickAddButton = ({publication, publicationList}) => {
    const {id: publicationListID, publication_list: publications} = publicationList;
    const isIncluded = publications.includes(publication.id);
    const {mutate, isLoading} = useToggleMutation(publicationListID, publication.id, isIncluded);
    const title = interpolate(isIncluded ? RemoveLabel : AddLabel, publicationList);
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

const QuickAddButtonController = ({publication, lastUpdatedPublicationList}) => {
    if (lastUpdatedPublicationList === null) return null;

    return <QuickAddButton publication={publication} publicationList={lastUpdatedPublicationList} />;
};

export default QuickAddButtonController;
