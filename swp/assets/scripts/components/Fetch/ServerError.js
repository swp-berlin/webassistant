import {faHeartbeat, faSadTear} from '@fortawesome/free-solid-svg-icons';

import _ from 'utils/i18n';

import RecoverableError from './RecoverableError';

export const Fallback = {
    icon: faSadTear,
    title: _('Server Error'),
    description: _('Something went wrong on our side…'),
};

export const Maintenance = {
    icon: faHeartbeat,
    title: _('Maintenance'),
    description: _('We are currently doing maintenance work. Please reload the page in a few seconds.'),
};

export const Errors = {
    502: Maintenance,
    503: Maintenance,
};

const ServerError = props => (
    <RecoverableError
        Errors={Errors}
        Fallback={Fallback}
        {...props}
    />
);

export default ServerError;
