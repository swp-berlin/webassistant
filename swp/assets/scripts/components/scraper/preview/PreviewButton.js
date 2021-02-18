import {useEffect} from 'react';
import {Button} from '@blueprintjs/core';

import {useMutationResult} from 'components/Fetch';
import {setErrors} from 'utils/form';


const PreviewButton = ({form, onPreview}) => {
    const [mutate, {success, result}] = useMutationResult(
        '/preview/',
        {
            method: 'POST',
            handleSuccess: () => {},
            setErrors: errors => setErrors(form.setError, errors),
        },
    );

    const handleClick = form.handleSubmit(data => mutate(data));

    useEffect(() => {
        if (success) onPreview(result.data);
    }, [onPreview, result.data, success]);

    return <Button className="lg:float-right" type="button" text="Preview" onClick={handleClick} />;
};

export default PreviewButton;
