import {useMutation} from 'hooks/query';
import {Button} from '@blueprintjs/core';
import {useCallback, useEffect} from 'react';


const PreviewButton = ({form, onPreview}) => {
    const [mutate, {success, result}] = useMutation('/preview/');

    const handleClick = useCallback(async () => {
        const valid = await form.trigger();

        if (valid) mutate(form.getValues());
    }, [form, mutate]);

    useEffect(() => {
        if (success) onPreview(result.data);
    }, [onPreview, result.data, success]);

    return <Button type="button" text="Preview" onClick={handleClick} />;
};

export default PreviewButton;
