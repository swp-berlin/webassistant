import {Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {showToast} from 'utils/toaster';

import {ActivationButton} from 'components/buttons';
import {DefaultHandlers} from 'components/Fetch/Form';

const ActivatedMessage = _('Monitor has been activated');
const DeactivatedMessage = _('Monitor has been deactivated');

const MutationOptions = {
    handleClientError(status, errors, ...args) {
        if (status === 400 && errors) {
            return Object.values(errors).forEach(messages => {
                messages.forEach(message => {
                    showToast(message, Intent.DANGER);
                });
            });
        }

        return DefaultHandlers.handleClientError(status, errors, ...args);
    },
};

const MonitorActivationButton = props => (
    <ActivationButton
        {...props}
        activatedMessage={ActivatedMessage}
        deactivatedMessage={DeactivatedMessage}
        mutationOptions={MutationOptions}
    />
);

export default MonitorActivationButton;
