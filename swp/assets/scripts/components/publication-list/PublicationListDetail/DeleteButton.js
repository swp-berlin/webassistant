import {useCallback, useState} from 'react';
import {useQueryClient} from 'react-query';
import {useNavigate} from 'react-router-dom';
import {Alert, Button, Intent} from '@blueprintjs/core';

import {buildAPIURL} from 'utils/api';
import _, {interpolate} from 'utils/i18n';
import Toaster from 'utils/toaster';

import {useMutation} from 'hooks/react-query';

import {Endpoint} from '../PublicationList';

const RedirectURL = '/search/publication-list/';

const CancelButtonText = _('Cancel');
const ConfirmButtonText = _('Delete');
const ConfirmMessage = _('Are you sure you want to delete publication list %(name)s?');
const ButtonTitle = _('Delete publication list %(name)s');
const SuccessMessage = _('Successfully deleted publication list %(name)s.');

const DeleteButton = ({id, name}) => {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const url = buildAPIURL(Endpoint, id);
    const {mutate, isLoading} = useMutation(url, 'DELETE', {
        onSuccess() {
            Toaster.show({
                message: interpolate(SuccessMessage, {name}),
                intent: Intent.SUCCESS,
            });

            queryClient.setQueryData(Endpoint, publicationLists => (
                publicationLists && publicationLists.filter(publicationList => publicationList.id !== id)
            ));

            navigate(RedirectURL);
        },
    });
    const [isOpen, setIsOpen] = useState(false);
    const buttonTitle = interpolate(ButtonTitle, {name});
    const confirmMessage = interpolate(ConfirmMessage, {name});
    const handleClick = useCallback(() => setIsOpen(true), [setIsOpen]);
    const handleCancel = useCallback(() => setIsOpen(false), [setIsOpen]);
    const handleConfirm = useCallback(() => mutate(), [mutate]);
    const baseProps = {
        icon: 'trash',
        loading: isLoading,
        intent: Intent.DANGER,
    };
    const alertProps = {
        ...baseProps,
        isOpen,
        cancelButtonText: CancelButtonText,
        confirmButtonText: ConfirmButtonText,
        onCancel: handleCancel,
        onConfirm: handleConfirm,
    };

    return (
        <>
            <Button {...baseProps} title={buttonTitle} onClick={handleClick} />
            <Alert {...alertProps} canEscapeKeyCancel canOutsideClickCancel>
                <p>{confirmMessage}</p>
            </Alert>
        </>
    );
};

export default DeleteButton;
