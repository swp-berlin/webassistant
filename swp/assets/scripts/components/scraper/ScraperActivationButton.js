import {useEffect} from 'react';
import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {useMutationResult} from 'components/Fetch';

const ActivateLabel = _('Activate');
const DeactivateLabel = _('Deactivate');
const ActivatedMessage = _('Scraper has been activated.');
const DeactivatedMessage = _('Scraper has been deactivated.');


const ScraperActivationButton = ({id, isActive, form, onToggle}) => {
    const [mutate, {success, result: {data}}] = useMutationResult(
        `/scraper/${id}/activate/`,
        {
            handleSuccess: ({is_active: isActive}) => ({
                intent: 'success',
                message: isActive ? ActivatedMessage : DeactivatedMessage,
            }),
            method: 'POST',
        },
        [],
    );

    const handleClick = form.handleSubmit(async data => {
        await mutate({...data, is_active: !isActive});
    });

    useEffect(() => {
        if (success) onToggle(data.is_active);
    }, [data, onToggle, success]);

    return <Button intent={Intent.PRIMARY} onClick={handleClick} text={isActive ? DeactivateLabel : ActivateLabel} />;
};

export default ScraperActivationButton;
