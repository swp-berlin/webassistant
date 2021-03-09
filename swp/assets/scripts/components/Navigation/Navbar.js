import {Alignment, Navbar as BlueprintNavbar} from '@blueprintjs/core';

import Breadcrumbs from './Breadcrumbs';
import LogoutLink from './LogoutLink';

const Navbar = ({breadcrumbs}) => (
    <BlueprintNavbar fixedToTop>
        <div className="container mx-auto">
            <BlueprintNavbar.Group align={Alignment.LEFT}>
                <Breadcrumbs items={breadcrumbs} />
            </BlueprintNavbar.Group>
            <BlueprintNavbar.Group align={Alignment.RIGHT}>
                <LogoutLink />
            </BlueprintNavbar.Group>
        </div>
    </BlueprintNavbar>
);

export default Navbar;
