import _ from 'utils/i18n';

import Page from 'components/Page';
import Query from 'components/Query';
import {useBreadcrumb} from 'components/Navigation';

import PublicationList from './PublicationList';
import PublicationListAddForm from './PublicationListAddForm';

const Search = _('Search');
export const Title = _('Publication Lists');
export const Endpoint = 'publication-list';

const PublicationListPage = () => {
    useBreadcrumb('/search/', Search);
    useBreadcrumb('/search/publication-list/', Title);

    return (
        <Page title={Title}>
            <Query queryKey={Endpoint}>
                {publicationLists => <PublicationList publicationLists={publicationLists} />}
            </Query>
            <PublicationListAddForm endpoint={Endpoint} />
        </Page>
    );
};

export default PublicationListPage;
