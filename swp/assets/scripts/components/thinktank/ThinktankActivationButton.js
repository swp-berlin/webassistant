import {Intent} from '@blueprintjs/core';

import _, {interpolate, ngettext} from 'utils/i18n';
import Toaster from 'utils/toaster';

import {ActivationButton} from 'components/buttons';
import {useQueryClient} from 'react-query';

const ActivatedMessage = _('Thinktank successfully activated.');
const DeactivatedMessage = _('Thinktank successfully deactivated.');

export const showIncompatibleScraperWarning = data => {
    const {domain, deactivated_scrapers: count} = data;

    if (!count) return;

    const message = ngettext(
        'Deactivated %(count)s scraper because its start url is not a subdomain of %(domain)s.',
        'Deactivated %(count)s scrapers because their start url is not a subdomain of %(domain)s.',
        count,
    );

    Toaster.show({
        intent: Intent.WARNING,
        message: interpolate(message, {count, domain}),
        timeout: 8 * 1000,
    });
};

const ThinktankActivationButton = ({id, endpoint, isActive, disabled}) => {
    const queryClient = useQueryClient();

    return (
        <ActivationButton
            endpoint={endpoint}
            isActive={isActive}
            disabled={disabled}
            activatedMessage={ActivatedMessage}
            deactivatedMessage={DeactivatedMessage}
            mutationOptions={{
                handleSuccess(data) {
                    queryClient.setQueryData(['thinktank', id], data);
                    showIncompatibleScraperWarning(data);
                },
            }}
        />
    );
};

export default ThinktankActivationButton;
