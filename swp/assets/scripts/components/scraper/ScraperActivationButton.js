import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {useMutationForm} from 'components/Fetch';
import {useEffect} from 'react';


const EnableLabel = _('Enable');
const DisableLabel = _('Disable');
const DisabledMessage = _('Scraper has been disabled.');
const EnabledMessage = _('Scraper has been enabled.');


const handleSuccess = ({is_active: isActive}) => ({
    intent: 'success',
    message: isActive ? EnabledMessage : DisabledMessage,
});


const ScraperActivationButton = ({id, initialIsActive}) => {
    const [onSubmit, {register, watch, setValue}, {success, result: {data}}] = useMutationForm(
        `/scraper/${id}/`,
        {defaultValues: {is_active: !initialIsActive}},
        {method: 'PATCH', handleSuccess},
    );

    useEffect(() => register('is_active'), [register]);

    useEffect(() => {
        if (success) setValue('is_active', !data.is_active);
    }, [success, data, setValue]);

    const active = watch('is_active', !initialIsActive);

    return <Button onClick={onSubmit} intent="primary" text={!active ? DisableLabel : EnableLabel} />;
};

export default ScraperActivationButton;
