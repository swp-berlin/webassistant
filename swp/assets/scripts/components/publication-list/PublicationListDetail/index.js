import {useEffect, useState} from 'react';

import _, {interpolate} from 'utils/i18n';

import {useQuery} from 'hooks/query';

import Page from 'components/Page';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';

import {Title} from '../PublicationList';
import PublicationListDetail from './PublicationListDetail';
import ExportButton from './ExportButton';
import EditableTitle from './EditableTitle';

const FallbackTitle = _('Publication List %(id)s');

const getTitle = (id, data) => (data ? data.name : interpolate(FallbackTitle, {id}));

const PublicationListDetailPage = ({id, url}) => {
    const endpoint = `/publication-list/${id}/`;
    const query = useQuery(endpoint);
    const {result: {data}, success} = query;
    const [title, setTitle] = useState(() => getTitle(id, data));
    const actions = [
        <ExportButton key="export" id={id} />,
    ];

    useBreadcrumb('..', Title);
    useBreadcrumb(url, title);

    useEffect(() => { setTitle(getTitle(id, data)); }, [id, data]);

    return (
        <Page title={success ? <EditableTitle id={id} title={title} setTitle={setTitle} /> : title} actions={actions}>
            <Result query={query}>
                {publicationList => <PublicationListDetail {...publicationList} />}
            </Result>
        </Page>
    );
};

export default PublicationListDetailPage;
