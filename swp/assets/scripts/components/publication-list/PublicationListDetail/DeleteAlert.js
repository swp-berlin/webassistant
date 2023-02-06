import {useCallback, useState} from 'react';
import {Alert, Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {useMutation} from 'hooks/react-query';

const CancelButtonText = _('Cancel');
const ConfirmButtonText = _('Delete');

const DefaultIcon = 'trash';
const DefaultIntent = Intent.DANGER;

const AlertProps = {
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

const DeleteAlertManager = props => {
    const {
        url,
        method = 'DELETE',
        icon = DefaultIcon,
        intent = DefaultIntent,
        onDelete,
        ...buttonProps
    } = props;

    const {
        buttonTitle,
        buttonIcon = icon,
        buttonIntent = intent,
        ...alertProps
    } = buttonProps;

    const [isOpen, setIsOpen] = useState(false);
    const {mutate, isLoading} = useMutation(url, method, {onSuccess: onDelete});
    const handleClick = useCallback(() => setIsOpen(true), [setIsOpen]);
    const handleCancel = useCallback(() => setIsOpen(false), [setIsOpen]);
    const handleConfirm = useCallback(() => mutate(), [mutate]);

    return (
        <>
            <Button
                title={buttonTitle}
                loading={isLoading}
                onClick={handleClick}
                intent={buttonIntent}
                icon={buttonIcon}
            />
            <DeleteAlert
                isOpen={isOpen}
                loading={isLoading}
                intent={intent}
                icon={icon}
                onConfirm={handleConfirm}
                onCancel={handleCancel}
                {...alertProps}
            />
        </>
    );
};

export default DeleteAlertManager;
