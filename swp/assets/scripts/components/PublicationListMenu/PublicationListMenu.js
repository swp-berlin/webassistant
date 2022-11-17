import {useCallback, useState} from 'react';
import {Button, ButtonGroup} from '@blueprintjs/core';

import _ from 'utils/i18n';

import QuickAddButton from './QuickAddButton';
import PublicationListDialog from './PublicationListDialog';

const ButtonTitle = _('Open publication list menu');

const PublicationListMenu = ({id: publicationID, publicationLists}) => {
    const [isOpen, setIsOpen] = useState(false);
    const handleClick = useCallback(() => setIsOpen(open => !open), [setIsOpen]);
    const handleClose = useCallback(() => setIsOpen(false), [setIsOpen]);
    const dialogProps = {
        isOpen,
        publicationID,
        publicationLists,
        onClose: handleClose,
    };

    return (
        <aside className="absolute right-0 top-0">
            <ButtonGroup vertical>
                <PublicationListDialog {...dialogProps}>
                    <Button icon={isOpen ? 'cross' : 'menu'} title={ButtonTitle} onClick={handleClick} />
                </PublicationListDialog>
                {publicationLists.length > 0 && (
                    <QuickAddButton
                        publicationID={publicationID}
                        publicationLists={publicationLists}
                    />
                )}
            </ButtonGroup>
        </aside>
    );
};

export default PublicationListMenu;
