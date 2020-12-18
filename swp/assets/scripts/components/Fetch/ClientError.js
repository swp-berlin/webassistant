import {Link} from 'react-router-dom';
import {faHandPaper, faSadTear, faSearch} from '@fortawesome/free-solid-svg-icons';

import _ from 'utils/i18n';

import BaseError from './BaseError';

export const Fallback = {
    icon: faSadTear,
    title: _('Client Error'),
    description: _("We couldn't handle the data your client send us."),
};

export const Unauthorized = {
    icon: faHandPaper,
    title: _('Unauthorized'),
    description: _('You have to be logged in to see this page.'),
    action: (
        <Link to="/login/">
            {_('Login')}
        </Link>
    ),
};

export const Forbidden = {
    icon: faHandPaper,
    title: _('Forbidden'),
    description: _('You have no permission to request this page.'),
};

export const NotFound = {
    icon: faSearch,
    title: _('Not found'),
    description: _("These aren't the droids you're looking for."),
};

export const Errors = {
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
};

const ClientError = props => (
    <BaseError
        Errors={Errors}
        Fallback={Fallback}
        {...props}
    />
);

export default ClientError;
