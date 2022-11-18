import {useCallback, useState} from 'react';
import {Alert, Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {useMutation} from 'hooks/react-query';

const CancelButtonText = _('Cancel');
const ConfirmButtonText = _('Delete');

const BaseProps = {
    icon: 'trash',
    intent: Intent.DANGER,
};

const AlertProps = {
    ...BaseProps,
    cancelButtonText: CancelButtonText,
    confirmButtonText: ConfirmButtonText,
    canEscapeKeyCancel: true,
    canOutsideClickCancel: true,
};

const DeleteAlert = ({confirmMessage, ...props}) => (
    <Alert {...AlertProps} {...props}>
        <p>{confirmMessage}</p>
    </Alert>
);

const DeleteAlertManager = ({url, method = 'DELETE', buttonTitle, confirmMessage, onDelete, ...props}) => {
    const [isOpen, setIsOpen] = useState(false);
    const {mutate, isLoading} = useMutation(url, method, {onSuccess: onDelete});
    const handleClick = useCallback(() => setIsOpen(true), [setIsOpen]);
    const handleCancel = useCallback(() => setIsOpen(false), [setIsOpen]);
    const handleConfirm = useCallback(() => mutate(), [mutate]);
    const {buttonIntent = BaseProps.intent} = props;

    return (
        <>
            <Button
                {...BaseProps}
                title={buttonTitle}
                loading={isLoading}
                onClick={handleClick}
                intent={buttonIntent}
            />
            <DeleteAlert
                isOpen={isOpen}
                loading={isLoading}
                confirmMessage={confirmMessage}
                onConfirm={handleConfirm}
                onCancel={handleCancel}
                {...props}
            />
        </>
    );
};

export default DeleteAlertManager;
