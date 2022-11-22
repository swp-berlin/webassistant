import {useCallback} from 'react';
import {useQueryClient} from 'react-query';
import {useNavigate} from 'react-router-dom';
import {Intent} from '@blueprintjs/core';

import {buildAPIURL} from 'utils/api';
import _, {interpolate} from 'utils/i18n';
import Toaster from 'utils/toaster';

import {Endpoint} from '../PublicationList';
import DeleteAlert from './DeleteAlert';

const RedirectURL = '/search/publication-list/';

const ConfirmMessage = _('Are you sure you want to delete publication list %(name)s?');
const ButtonTitle = _('Delete publication list %(name)s');
const SuccessMessage = _('Successfully deleted publication list %(name)s.');

const DeleteButton = ({id, name}) => {
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const url = buildAPIURL(Endpoint, id);
    const buttonTitle = interpolate(ButtonTitle, {name});
    const confirmMessage = interpolate(ConfirmMessage, {name});
    const handleDelete = useCallback(
        () => {
            Toaster.show({
                message: interpolate(SuccessMessage, {name}),
                intent: Intent.SUCCESS,
            });

            queryClient.setQueryData(Endpoint, publicationLists => (
                publicationLists && publicationLists.filter(publicationList => publicationList.id !== id)
            ));

            navigate(RedirectURL);
        },
        [id, name, queryClient, navigate],
    );

    return (
        <DeleteAlert
            url={url}
            buttonTitle={buttonTitle}
            confirmMessage={confirmMessage}
            onDelete={handleDelete}
        />
    );
};

export default DeleteButton;
