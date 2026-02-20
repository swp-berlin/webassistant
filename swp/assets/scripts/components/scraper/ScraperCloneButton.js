import {useCallback} from 'react';

import {Button} from "@blueprintjs/core";

import _ from 'utils/i18n';

import {useMutationResult} from 'components/Fetch';

const StartedMessage = _('Scraper has been started.');

const handleSuccess = () => ({
    intent: 'success',
    message: StartedMessage,
});

const ScraperCloneButton = ({id}) => {
    const endpoint = `/scraper/${id}/clone/`;

    const mutationOptions = {
        method: 'POST',
        handleSuccess,
    };
    const [mutate, {result: {data}, loading}] = useMutationResult(endpoint, mutationOptions, []);
    const handleClick = useCallback( () => mutate({...data}), [data]);

    return <Button loading={loading} onClick={handleClick} text={'⿻'}/>;
};

export default ScraperCloneButton;
