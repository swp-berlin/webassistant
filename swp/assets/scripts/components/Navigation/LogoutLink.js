import _ from 'utils/i18n';
import BaseLink from './BaseLink';


const Label = _('Log out');

const LogoutLink = () => (
    <BaseLink to="/logout/" icon="log-out">
        {Label}
    </BaseLink>
);

export default LogoutLink;
