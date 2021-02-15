import {useEffect, useMemo, useState} from 'react';
import {useQuery} from 'hooks/query';


export const useUpdatePublicationsQuery = (endpoint, paramsProvided) => {
    const [updatePublications, setUpdatePublications] = useState(false);
    const params = useMemo(
        () => ({update_publications: updatePublications, ...paramsProvided}),
        [paramsProvided, updatePublications],
    );
    const result = useQuery(endpoint, params);
    const {success, called} = result;

    useEffect(() => {
        if (called && success) setUpdatePublications(true);
    }, [success, called]);

    return result;
};
