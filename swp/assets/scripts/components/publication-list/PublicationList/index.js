import _ from 'utils/i18n';

import Page from 'components/Page';
import {Query} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';

import PublicationList from './PublicationList';

export const Title = _('Publication Lists');

const PublicationListPage = ({url}) => {
    useBreadcrumb(url, Title);

    return (
        <Page title={Title}>
            <Query endpoint="publication-list">
                {publicationLists => <PublicationList publicationLists={publicationLists} />}
            </Query>
        </Page>
    );
};

export default PublicationListPage;
