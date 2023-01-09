import {useCallback, useState} from 'react';
import {Button, Popover} from '@blueprintjs/core';

import _ from 'utils/i18n';

import PublicationListDialogContent from './PublicationListDialogContent';

const ButtonTitle = _('Open publication list menu');

const PublicationListDialog = ({publication, publicationLists, lastUpdatedPublicationList}) => {
    const [isOpen, setIsOpen] = useState(false);
    const handleClick = useCallback(() => setIsOpen(open => !open), [setIsOpen]);
    const handleClose = useCallback(() => setIsOpen(false), [setIsOpen]);
    const popoverProps = {isOpen, publication, publicationLists};

    return (
        <Popover {...popoverProps} placement="left-start" onClose={handleClose}>
            <Button icon={isOpen ? 'cross' : 'menu'} title={ButtonTitle} onClick={handleClick} />
            <PublicationListDialogContent
                publication={publication}
                publicationLists={publicationLists}
                lastUpdatedPublicationList={lastUpdatedPublicationList}
            />
        </Popover>
    );
};

export default PublicationListDialog;
