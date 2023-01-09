import {useCallback} from 'react';
import classNames from 'classnames';
import {Checkbox, Spinner} from '@blueprintjs/core';

import DefaultTag from 'components/DefaultTag';

import {useToggleMutation} from './hooks';

const Label = ({name, isLoading, isDefault}) => (
    <>
        {isLoading && <Spinner size={12} />}
        <span>{name}</span>
        {isDefault && <DefaultTag />}
    </>
);

const PublicationListDialogItem = props => {
    const {publicationID, id: publicationListID, publication_list: publications, name, isLastUpdated} = props;
    const isIncluded = publications.includes(publicationID);
    const {mutate, isLoading} = useToggleMutation(publicationListID, publicationID, isIncluded);
    const handleChange = useCallback(() => mutate(), [mutate]);

    return (
        <li className={classNames('publication-list-menu-item', {'is-included': isIncluded})}>
            <Checkbox
                className="mb-1"
                checked={isIncluded}
                labelElement={(
                    <Label
                        name={name}
                        isLoading={isLoading}
                        isDefault={isLastUpdated}
                    />
                )}
                onChange={handleChange}
                disabled={isLoading}
            />
        </li>
    );
};

export default PublicationListDialogItem;
