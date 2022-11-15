import {useCallback, useState} from 'react';
import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';

import QuickAddButton from './QuickAddButton';
import PublicationListDialog from './PublicationListDialog';

const ButtonTitle = _('Open publication list menu');

const PublicationListMenu = ({id: publicationID, publicationLists}) => {
    const [open, setOpen] = useState(false);
    const handleOpen = useCallback(() => setOpen(true), [setOpen]);
    const handleClose = useCallback(() => setOpen(false), [setOpen]);

    return (
        <aside className="absolute right-0 top-0">
            {publicationLists.length > 0 && (
                <QuickAddButton
                    publicationID={publicationID}
                    publicationLists={publicationLists}
                />
            )}
            {open || <Button icon="menu" title={ButtonTitle} onClick={handleOpen} />}
            {open && (
                <PublicationListDialog
                    publicationID={publicationID}
                    publicationLists={publicationLists}
                    onClose={handleClose}
                />
            )}
        </aside>
    );
};

export default PublicationListMenu;
