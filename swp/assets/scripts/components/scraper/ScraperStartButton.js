import {useCallback} from 'react';
import {useQueryClient} from 'react-query';

import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {buildURL} from 'utils/url';

import {useMutationResult} from 'components/Fetch';
import Query from 'components/Query';

const StartedMessage = _('Scraper has been started.');
const Run = _('Run');

const RefetchInterval = 1000;

const MutationOptions = {
    method: 'POST',
    handleSuccess() {
        return {
            intent: 'success',
            message: StartedMessage,
        };
    },
};

const getData = (id, thinktankID, isRunning) => ({
    id,
    thinktank_id: thinktankID,
    is_running: isRunning,
});

const updateScraperData = (queryClient, scraperData) => {
    const {id, thinktank_id: thinktankID, is_running: isRunning} = scraperData;

    if (!isRunning) return;

    queryClient.setQueryData(['thinktank', thinktankID], thinktankData => ({
        ...thinktankData,
        scrapers: thinktankData.scrapers.map(scraper => (
            scraper.id === id ? {...scraper, ...scraperData} : scraper
        )),
    }));
};

const ScraperStartButton = ({id, thinktankID, isRunning}) => {
    const queryClient = useQueryClient();
    const mutationEndpoint = buildURL('scraper', id, 'scrape');
    const [mutate, {loading}] = useMutationResult(mutationEndpoint, MutationOptions, []);
    const handleClick = useCallback(
        () => {
            const data = getData(id, thinktankID, true);

            mutate(data);
            updateScraperData(queryClient, data);
        },
        [id, thinktankID, mutate, queryClient],
    );
    const queryOptions = {
        queryKey: ['scraper', id, 'info'],
        enabled: isRunning,
        refetchInterval: RefetchInterval,
        initialData: getData(id, thinktankID, isRunning),
        onSuccess(scraperData) {
            updateScraperData(queryClient, scraperData);
        },
    };

    return (
        <Query {...queryOptions}>
            {({is_running: isRunning}) => (
                <Button text={Run} loading={loading} disabled={isRunning} onClick={handleClick} />
            )}
        </Query>
    );
};

export default ScraperStartButton;
