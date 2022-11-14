import {useEffect, useState} from 'react';
import {useQuery} from 'react-query';

import _, {interpolate} from 'utils/i18n';

import Page from 'components/Page';
import {QueryResult} from 'components/Query';
import {useBreadcrumb} from 'components/Navigation';

import {Endpoint, Title} from '../PublicationList';
import PublicationListDetail from './PublicationListDetail';
import ExportButton from './ExportButton';
import EditableTitle from './EditableTitle';

const FallbackTitle = _('Publication List %(id)s');

const getTitle = (id, data) => (data ? data.name : interpolate(FallbackTitle, {id}));

const PublicationListDetailPage = ({id, url}) => {
    const queryKey = [Endpoint, id];
    const query = useQuery(queryKey);
    const {data, isSuccess} = query;
    const [title, setTitle] = useState(() => getTitle(id, data));
    const actions = [
        isSuccess && <ExportButton key="export" id={id} />,
    ];

    useBreadcrumb('..', Title);
    useBreadcrumb(url, title);

    useEffect(() => { setTitle(getTitle(id, data)); }, [id, data]);

    return (
        <Page title={isSuccess ? <EditableTitle id={id} title={title} setTitle={setTitle} /> : title} actions={actions}>
            <QueryResult query={query}>
                {publicationList => <PublicationListDetail {...publicationList} />}
            </QueryResult>
        </Page>
    );
};

export default PublicationListDetailPage;
