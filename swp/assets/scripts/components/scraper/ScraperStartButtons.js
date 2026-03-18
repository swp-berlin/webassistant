import {Fragment, useCallback} from 'react';
import {useQueryClient} from 'react-query';

import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {buildURL} from 'utils/url';
import {preventDefault} from 'utils/event';

import {useMutationResult} from 'components/Fetch';
import Query from 'components/Query';

const StartedMessage = _('Scraper has been started.');
const Run = _('Run');
const ForceUpdate = _('Update');

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

const getData = (id, thinktankID, isActive, isRunning) => ({
    id,
    thinktank_id: thinktankID,
    is_active: isActive,
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

const ScraperStartButton = ({forceUpdate, onClick, ...props}) => {
    const handleClick = useCallback(
        event => {
            preventDefault(event);

            return onClick(forceUpdate);
        },
        [forceUpdate, onClick],
    );

    props.text = forceUpdate ? ForceUpdate : Run;
    props.icon = forceUpdate ? 'refresh' : 'play';

    return <Button {...props} onClick={handleClick} />;
};

const ScraperStartButtons = ({id, thinktankID, isActive, isRunning}) => {
    const queryClient = useQueryClient();
    const mutationEndpoint = buildURL('scraper', id, 'scrape');
    const [mutate, {loading}] = useMutationResult(mutationEndpoint, MutationOptions, []);
    const handleClick = useCallback(
        (forceUpdate = false) => {
            const data = getData(id, thinktankID, isActive, true);

            mutate({force_update: forceUpdate});
            updateScraperData(queryClient, data);
        },
        [id, thinktankID, isActive, mutate, queryClient],
    );
    const queryOptions = {
        queryKey: ['scraper', id, 'info'],
        enabled: isActive && isRunning,
        refetchInterval: RefetchInterval,
        initialData: getData(id, thinktankID, isActive, isRunning),
        onSuccess(scraperData) {
            updateScraperData(queryClient, scraperData);
        },
    };

    const buttonProps = {
        loading,
        onClick: handleClick,
    };

    return (
        <Query {...queryOptions}>
            {({is_active: isActive, is_running: isRunning}) => (
                <Fragment>
                    <ScraperStartButton {...buttonProps} disabled={isActive ? isRunning : true} />
                    <ScraperStartButton {...buttonProps} disabled={isActive ? isRunning : true} forceUpdate />
                </Fragment>
            )}
        </Query>
    );
};

export default ScraperStartButtons;
