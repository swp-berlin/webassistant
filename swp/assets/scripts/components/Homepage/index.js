import Page from 'components/Page';

import {usePermission} from 'hooks/user';
import MonitorLink from './MonitorLink';
import ThinktankLink from './ThintankLink';
import NoPermission from './NoPermission';

const Homepage = () => {
    const viewThinktanks = usePermission('swp.view_thinktank');
    const viewMonitors = usePermission('swp.view_monitor');

    return (
        <Page className="flex min-h-full justify-center items-center">
            <div className="flex justify-center space-x-5">
                {viewThinktanks && <ThinktankLink />}
                {viewMonitors && <MonitorLink />}
                {viewThinktanks || viewMonitors || <NoPermission />}
            </div>
        </Page>
    );
};

export default Homepage;
