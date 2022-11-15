import {useQuery} from 'react-query';
import {useParams} from 'react-router-dom';

import _, {interpolate} from 'utils/i18n';

import {QueryResult} from 'components/Query';
import {useBreadcrumb} from 'components/Navigation';

import {Endpoint, Title} from '../PublicationList';
import PublicationListDetail from './PublicationListDetail';

const FallbackTitle = _('Publication List %(id)s');

const getTitle = (id, data) => (data ? data.name : interpolate(FallbackTitle, {id}));

const PublicationListDetailPage = () => {
    const {id} = useParams();
    const queryKey = [Endpoint, +id];
    const query = useQuery(queryKey);

    useBreadcrumb('/publication-list/', Title);
    useBreadcrumb(`/publication-list/${id}/`, getTitle(id, query.data));

    return (
        <QueryResult query={query}>
            {publicationList => <PublicationListDetail {...publicationList} />}
        </QueryResult>
    );
};

export default PublicationListDetailPage;
