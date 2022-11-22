import {useQueryClient} from 'react-query';
import findIndex from 'lodash/findIndex';

import {buildAPIURL} from 'utils/api';

import {useMutation} from 'hooks/react-query';

const Endpoint = 'publication-list';

const onAddSuccess = (queryClient, data) => {
    queryClient.setQueryData(Endpoint, ([...publicationLists]) => {
        const index = findIndex(publicationLists, {id: data.id});

        if (index >= 0) publicationLists.splice(index, 1);

        return [data, ...publicationLists];
    });
};

const onRemoveSuccess = (queryClient, data) => {
    queryClient.setQueryData(Endpoint, publicationLists => (
        publicationLists.map(publicationList => (
            publicationList.id === data.id ? data : publicationList
        ))
    ));
};

export const useToggleMutation = (publicationListID, publicationID, isIncluded) => {
    const queryClient = useQueryClient();
    const action = isIncluded ? 'remove' : 'add';
    const url = buildAPIURL(Endpoint, publicationListID, action, publicationID);

    return useMutation(url, 'POST', {
        onSuccess(data) {
            (isIncluded ? onRemoveSuccess : onAddSuccess)(queryClient, data);
        },
    });
};
