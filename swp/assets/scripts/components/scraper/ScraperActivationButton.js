import {useEffect} from 'react';
import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {setErrors} from 'utils/form';

import {useMutationResult} from 'components/Fetch';

const ActivateLabel = _('Activate');
const DeactivateLabel = _('Deactivate');
const ActivatedMessage = _('Scraper has been activated.');
const DeactivatedMessage = _('Scraper has been deactivated.');

const handleSuccess = ({is_active: isActive}) => ({
    intent: 'success',
    message: isActive ? ActivatedMessage : DeactivatedMessage,
});

const ScraperActivationButton = ({id, isActive, form, onToggle}) => {
    const endpoint = `/scraper/${id}/activate/`;
    const mutationOptions = {
        method: 'POST',
        handleSuccess,
        setErrors(errors) {
            setErrors(form.setError, errors);
        },
    };
    const [mutate, {success, result: {data}, loading}] = useMutationResult(endpoint, mutationOptions, []);
    const handleClick = form.handleSubmit(data => mutate({...data, is_active: !isActive}));
    const label = isActive ? DeactivateLabel : ActivateLabel;

    useEffect(() => {
        if (success) onToggle(data.is_active);
    }, [data, onToggle, success]);

    return <Button intent={Intent.PRIMARY} text={label} loading={loading} onClick={handleClick} />;
};

export default ScraperActivationButton;
