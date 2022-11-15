import {faWifi} from '@fortawesome/free-solid-svg-icons/faWifi';

import _ from 'utils/i18n';
import {NetworkError as NetworkErrorMessage} from 'swp/messages';

import RecoverableError from './RecoverableError';

export const DefaultProps = {
    icon: faWifi,
    title: _('Network Error'),
    description: NetworkErrorMessage,
};

const NetworkError = props => (
    <RecoverableError
        Fallback={DefaultProps}
        status={null}
        {...props}
    />
);

export default NetworkError;
