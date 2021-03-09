import {AnchorButton, Icon} from '@blueprintjs/core';

import {useUser} from 'hooks/user';
import _ from 'utils/i18n';

const Label = _('Log out');


const LogoutLink = () => {
    const {email} = useUser();

    return (
        <AnchorButton href="/logout/" minimal className="flex justify-between">
            <span className="hidden md:inline">{email}</span>
            <Icon icon="log-out" className="ml-2 mr-1" />
            {Label}
        </AnchorButton>
    );
};

export default LogoutLink;
