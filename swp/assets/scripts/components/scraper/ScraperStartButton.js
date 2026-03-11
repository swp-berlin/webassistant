import {useCallback, useState} from 'react';

import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {useMutationResult} from 'components/Fetch';
import Query from 'components/Query';

const StartedMessage = _('Scraper has been started.');
const Run = _('Run');

const handleSuccess = () => ({
    intent: 'success',
    message: StartedMessage,
});


const ScraperStartButton = ({id, refetchInterval, ...options}) => {
    const endpoint = `/scraper/${id}/scrape/`;
    const infoEndpoint = `/api/scraper/${id}/info`;
    const [currentRefetchInterval, setCurrentRefetchInterval] = useState(null);
    const mutationOptions = {
        method: 'POST',
        handleSuccess,
    };
    const [mutate, {result: {data}, loading}] = useMutationResult(endpoint, mutationOptions, []);

    const handleClick = useCallback(() => {
        mutate({...data});
        setCurrentRefetchInterval(refetchInterval);
    }, [setCurrentRefetchInterval, refetchInterval, mutate, data]);

    const onSuccess = useCallback(({isRunning}) => {
        setCurrentRefetchInterval(() => (isRunning || loading) ? refetchInterval : null);
    }, [setCurrentRefetchInterval, loading, refetchInterval]);

    return (
        <Query queryKey={infoEndpoint} refetchInterval={currentRefetchInterval} onSuccess={onSuccess}>
            {({isRunning}) => (
                <Button disabled={isRunning} loading={loading} onClick={handleClick} text={Run} {...options} />
            )}
        </Query>
    );
};

export default ScraperStartButton;
