import {cloneElement, useCallback, useState} from 'react';
import {Button, ButtonGroup} from '@blueprintjs/core';

import _ from 'utils/i18n';

import PublicationListDialog from './PublicationListDialog';

const ButtonTitle = _('Open publication list menu');

const PublicationListMenu = ({publication, publicationLists, children}) => {
    const [isOpen, setIsOpen] = useState(false);
    const handleClick = useCallback(() => setIsOpen(open => !open), [setIsOpen]);
    const handleClose = useCallback(() => setIsOpen(false), [setIsOpen]);
    const dialogProps = {
        isOpen,
        publication,
        publicationLists,
        onClose: handleClose,
    };

    return (
        <aside className="absolute right-0 top-0">
            <ButtonGroup vertical>
                <PublicationListDialog {...dialogProps}>
                    <Button icon={isOpen ? 'cross' : 'menu'} title={ButtonTitle} onClick={handleClick} />
                </PublicationListDialog>
                {children && cloneElement(children, {publication, publicationLists})}
            </ButtonGroup>
        </aside>
    );
};

export default PublicationListMenu;
