import {useCallback, useEffect, useState} from 'react';

import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {useMutationResult} from 'components/Fetch';
import {useQuery} from 'hooks/query';

const StartedMessage = _('Scraper has been started.');

const handleSuccess = () => ({
    intent: 'success',
    message: StartedMessage,
});

const ScraperStartButton = ({id, refetchInterval}) => {
    const endpoint = `/scraper/${id}/scrape/`;
    const isRunningEndpoint = `/scraper/${id}/is_running/`;

    const mutationOptions = {
        method: 'POST',
        handleSuccess,
    };

    const [mutate, {result: {data}, loading}] = useMutationResult(endpoint, mutationOptions, []);
    const handleClick = useCallback(() => mutate({...data}), [mutate, data]);
    const {result: {data: qdata}} = useQuery(isRunningEndpoint, {refetchInterval});

    return <Button disabled={qdata?.isRunning} loading={loading} onClick={handleClick} text="Start Scrape" />;
};

export default ScraperStartButton;
