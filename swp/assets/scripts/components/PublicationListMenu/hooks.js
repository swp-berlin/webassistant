import {useMemo} from 'react';
import {useQueryClient} from 'react-query';
import maxBy from 'lodash/maxBy';

import {buildAPIURL} from 'utils/api';

import {useMutation} from 'hooks/react-query';

const Endpoint = 'publication-list';

const updatePublicationLists = (queryClient, data) => {
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
            updatePublicationLists(queryClient, data);
        },
    });
};

const timeStamp = ({last_updated: lastUpdated}) => new Date(lastUpdated);

export const useLastUpdatedPublicationList = publicationLists => useMemo(
    () => (publicationLists.length ? maxBy(publicationLists, timeStamp) : null),
    [publicationLists],
);
