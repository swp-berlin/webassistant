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

const PublicationListMenuItem = ({publicationID, id: publicationListID, publication_list: publications, name}) => {
    const isIncluded = publications.includes(publicationID);
    const {mutate, isLoading} = useToggleMutation(publicationListID, publicationID, isIncluded);
    const handleChange = useCallback(() => mutate(), [mutate]);
    const label = <Label name={name} isLoading={isLoading} />;

    return (
        <li className={classNames('publication-list-menu-item', {'is-included': isIncluded})}>
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

export default PublicationListMenuItem;
