import {useParams} from 'react-router-dom';

import parseISO from 'date-fns/parseISO';
import format from 'date-fns/format';
import {de} from 'date-fns/locale';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faClock} from '@fortawesome/free-solid-svg-icons/faClock';

import _ from 'utils/i18n';

import {useQuery} from 'hooks/query';

import Page from 'components/Page';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import {usePoolBreadcrumb} from 'components/PoolBreadcrumb';
import {getThinktankLabel} from 'components/thinktank/helper';

import ScraperForm from './ScraperForm';
import ScraperActivationContainer from './ScraperActivationContainer';

const ScraperLabel = _('Scraper');
const Thinktanks = _('Thinktanks');

const LastRun = ({lastRun}) => (
    <div className="mt-2 flex items-center text-sm text-gray-500">
        <FontAwesomeIcon className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" icon={faClock} />
        {`Last run: ${format(parseISO(lastRun), 'PP pp', {locale: de})}`}
    </div>
);

const ScraperEdit = () => {
    const {id, thinktankID} = useParams();
    const endpoint = `/scraper/${id}/`;
    const query = useQuery(endpoint);
    const {loading, success, result: {data: scraper}} = query;
    const thinktankLabel = loading || !success ? getThinktankLabel(thinktankID, query) : scraper.thinktank.name;

    usePoolBreadcrumb(scraper);
    useBreadcrumb('/thinktank/', Thinktanks);
    useBreadcrumb(`/thinktank/${thinktankID}/`, thinktankLabel);
    useBreadcrumb(`/thinktank/${thinktankID}/scraper/${id}/`, ScraperLabel);

    return (
        <Result result={query}>
            {scraper => {
                const {last_run: lastRun} = scraper;
                const subtitle = lastRun && <LastRun lastRun={lastRun} />;
                const actions = <ScraperActivationContainer />;

                return (
                    <Page title={scraper.name} subtitle={subtitle} actions={actions}>
                        <ScraperForm endpoint={endpoint} data={scraper} />
                    </Page>
                );
            }}
        </Result>
    );
};

export default ScraperEdit;
