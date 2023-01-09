import Query from 'components/Query';

import {useLastUpdatedPublicationList} from './hooks';

import PublicationListMenu from './PublicationListMenu';
import PublicationListDialog from './PublicationListDialog';
import QuickAddButton from './QuickAddButton';

export {
    useLastUpdatedPublicationList,
    PublicationListDialog,
    QuickAddButton,
};

const NoLoadingAnimation = () => null;

const Options = {
    components: {
        loading: NoLoadingAnimation,
    },
};

const PublicationListMenuController = ({publication, children}) => (
    <Query queryKey="publication-list" {...Options}>
        {publicationLists => (
            <PublicationListMenu publication={publication} publicationLists={publicationLists}>
                {children}
            </PublicationListMenu>
        )}
    </Query>
);

export default PublicationListMenuController;
