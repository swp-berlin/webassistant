import Page from 'components/Page';

import {useUser} from 'hooks/user';
import AdminLink from './AdminLink';
import MonitorLink from './MonitorLink';
import SearchLink from './SearchLink';
import ThinktankLink from './ThintankLink';
import NoPermission from './NoPermission';

const Homepage = () => {
    const user = useUser();
    const viewThinktanks = user.hasPerm('swp.view_thinktank');
    const viewMonitors = user.hasPerm('swp.view_monitor');
    const viewSearch = user.hasPerm('swp.can_research');
    const viewAdmin = user.canViewAdmin();
    const hasAnyPermission = (
        viewSearch
        || viewMonitors
        || viewThinktanks
        || viewAdmin
    );

    return (
        <Page className="flex min-h-full justify-center items-center">
            <div className="flex justify-center items-center">
                {viewThinktanks && <ThinktankLink className="flex-1 block" />}
                {viewMonitors && <MonitorLink className="flex-1 block" />}
                {viewSearch && <SearchLink className="flex-1 block" />}
                {viewAdmin && <AdminLink className="flex-1 block" />}
                {hasAnyPermission || <NoPermission />}
            </div>
        </Page>
    );
};

export default Homepage;
