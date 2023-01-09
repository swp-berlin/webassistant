import {useCallback} from 'react';
import classNames from 'classnames';
import {Checkbox, Spinner} from '@blueprintjs/core';

import {useToggleMutation} from './hooks';

const Label = ({name, isLoading}) => (
    <>
        {isLoading && <Spinner size={12} />}
        <span>{name}</span>
    </>
);

const PublicationListDialogItem = props => {
    const {publicationID, id: publicationListID, publication_list: publications, name, isLastUpdated} = props;
    const isIncluded = publications.includes(publicationID);
    const {mutate, isLoading} = useToggleMutation(publicationListID, publicationID, isIncluded);
    const handleChange = useCallback(() => mutate(), [mutate]);
    const label = <Label name={name} isLoading={isLoading} />;
    const className = classNames('publication-list-menu-item', {
        'is-included': isIncluded,
        'is-last-updated': isLastUpdated,
    });

    return (
        <li className={className}>
            <Checkbox
                className="mb-1"
                checked={isIncluded}
                labelElement={label}
                onChange={handleChange}
                disabled={isLoading}
            />
        </li>
    );
};

export default PublicationListDialogItem;
