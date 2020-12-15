import {faWifi} from '@fortawesome/free-solid-svg-icons';

import _ from 'utils/i18n';

import RecoverableError from './RecoverableError';

export const DefaultProps = {
    icon: faWifi,
    title: _('Network Error'),
    description: _('A network error occurred. Please try again.'),
};

const NetworkError = props => (
    <RecoverableError
        Fallback={DefaultProps}
        status={null}
        {...props}
    />
);

export default NetworkError;
