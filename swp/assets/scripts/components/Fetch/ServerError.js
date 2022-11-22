import {faHeartbeat} from '@fortawesome/free-solid-svg-icons/faHeartbeat';
import {faSadTear} from '@fortawesome/free-solid-svg-icons/faSadTear';

import _ from 'utils/i18n';
import {
    ServerError as ServerErrorMessage,
    Maintenance as MaintenanceMessage,
} from 'swp/messages';

import RecoverableError from './RecoverableError';

export const Fallback = {
    icon: faSadTear,
    title: _('Server Error'),
    description: ServerErrorMessage,
};

export const Maintenance = {
    icon: faHeartbeat,
    title: _('Maintenance'),
    description: MaintenanceMessage,
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
