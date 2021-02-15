import {useCallback, useEffect} from 'react';
import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {useMutation} from 'hooks/query';


const ButtonLabel = _('Preview');

const PreviewButton = ({form, onPreview}) => {
    const [mutate, {loading, success, result}] = useMutation('/thinktankfilter/preview/');

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
