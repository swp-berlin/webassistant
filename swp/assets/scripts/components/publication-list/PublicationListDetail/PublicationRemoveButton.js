import {useQueryClient} from 'react-query';

import {buildAPIURL} from 'utils/api';
import _, {interpolate} from 'utils/i18n';

import {Endpoint} from '../PublicationList';
import DeleteAlert from './DeleteAlert';

const Title = _('Remove %(title)s from %(name)s');
const ConfirmButtonText = _('Remove');
const ConfirmMessage = _('Are you sure you want to remove the publication %(title)s from the list %(name)s?');

const PublicationRemoveButton = ({publicationList, publication}) => {
    const queryClient = useQueryClient();
    const url = buildAPIURL(Endpoint, publicationList.id, 'remove', publication.id);
    const context = {title: publication.title, name: publicationList.name};
    const buttonTitle = interpolate(Title, context);
    const confirmMessage = interpolate(ConfirmMessage, context);
    const handleDelete = data => {
        queryClient.setQueryData(Endpoint, publicationLists => (
            publicationLists.map(publicationList => (publicationList.id === data.id ? data : publicationList))
        ));
        queryClient.setQueryData([Endpoint, publicationList.id], ({publications, ...publicationList}) => ({
            publications: publications.filter(({id}) => id !== publication.id),
            ...publicationList,
            ...data,
        }));
    };

    return (
        <DeleteAlert
            url={url}
            method="POST"
            buttonTitle={buttonTitle}
            confirmButtonText={ConfirmButtonText}
            confirmMessage={confirmMessage}
            onDelete={handleDelete}
            buttonIntent={null}
        />
    );
};

export default PublicationRemoveButton;
