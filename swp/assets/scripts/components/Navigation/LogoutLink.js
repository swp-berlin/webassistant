import _ from 'utils/i18n';
import {AnchorButton} from '@blueprintjs/core';

const Label = _('Log out');

const LogoutLink = () => (
    <AnchorButton href="/logout/" icon="log-out" minimal>
        {Label}
    </AnchorButton>
);

export default LogoutLink;
