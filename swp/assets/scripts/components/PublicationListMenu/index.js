import Query from 'components/Query';

import PublicationListMenu from './PublicationListMenu';

const NoLoadingAnimation = () => null;

const Options = {
    components: {
        loading: NoLoadingAnimation,
    },
};

const PublicationListMenuController = ({id}) => (
    <Query queryKey="publication-list" {...Options}>
        {publicationLists => <PublicationListMenu id={id} publicationLists={publicationLists} />}
    </Query>
);

export default PublicationListMenuController;
