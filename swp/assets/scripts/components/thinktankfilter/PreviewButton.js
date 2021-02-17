import {useCallback, useEffect} from 'react';
import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {useMutationResult} from 'components/Fetch';
import {setErrors} from 'utils/form';


const ButtonLabel = _('Preview');

const PreviewButton = ({form, onPreview}) => {
    const [mutate, {loading, success, result}] = useMutationResult(
        '/thinktankfilter/preview/',
        {
            method: 'POST',
            handleSuccess: () => {},
            setErrors: errors => setErrors(form.setError, errors),
        },
    );

    const handleClick = useCallback(async () => {
        const valid = await form.trigger();

        if (valid) mutate(form.getValues());
    }, [form, mutate]);

    useEffect(() => {
        if (success) onPreview(result.data);
    }, [onPreview, result.data, success]);

    return <Button type="button" loading={loading} text={ButtonLabel} onClick={handleClick} />;
};

export default PreviewButton;
