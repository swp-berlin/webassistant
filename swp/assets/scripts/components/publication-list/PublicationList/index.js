import _ from 'utils/i18n';

import Page from 'components/Page';
import Query from 'components/Query';
import {useBreadcrumb} from 'components/Navigation';

import PublicationList from './PublicationList';

export const Title = _('Publication Lists');
export const Endpoint = 'publication-list';

const PublicationListPage = ({url}) => {
    useBreadcrumb(url, Title);

    return (
        <Page title={Title}>
            <Query queryKey={Endpoint}>
                {publicationLists => <PublicationList publicationLists={publicationLists} />}
            </Query>
        </Page>
    );
};

export default PublicationListPage;
