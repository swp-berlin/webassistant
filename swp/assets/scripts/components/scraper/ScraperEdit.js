import parseISO from 'date-fns/parseISO';
import format from 'date-fns/format';
import {de} from 'date-fns/locale';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faClock} from '@fortawesome/free-solid-svg-icons/faClock';

import {useQuery} from 'hooks/query';
import _ from 'utils/i18n';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import {ActivationButton} from 'components/buttons';
import {getThinktankLabel} from 'components/thinktank/helper';

import ScraperForm from './ScraperForm';


const ScraperLabel = _('Scraper');
const Thinktanks = _('Thinktanks');
const ActivatedMessage = _('Scraper has been activated.');
const DeactivatedMessage = _('Scraper has been deactivated.');

const LastRun = ({lastRun}) => (
    <div className="mt-2 flex items-center text-sm text-gray-500">
        <FontAwesomeIcon className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" icon={faClock} />
        {`Last run: ${format(parseISO(lastRun), 'PP pp', {locale: de})}`}
    </div>
);


const ScraperEdit = ({id, thinktankID}) => {
    const endpoint = `/scraper/${id}/`;
    const query = useQuery(endpoint);
    const {loading, success, result: {data: scraper}} = query;

    const thinktankLabel = loading || !success ? getThinktankLabel(thinktankID, query) : scraper.thinktank.name;

    useBreadcrumb('/thinktank/', Thinktanks);
    useBreadcrumb(`/thinktank/${thinktankID}/`, thinktankLabel);
    useBreadcrumb(endpoint, ScraperLabel);

    return (
        <Result result={query}>
            {({name, last_run: lastRun, is_active: isActive}) => (
                <Page
                    title={name}
                    subtitle={lastRun && <LastRun lastRun={lastRun} />}
                    actions={(
                        <ActivationButton
                            endpoint={`/scraper/${id}/`}
                            defaultIsActive={isActive}
                            activatedMessage={ActivatedMessage}
                            deactivatedMessage={DeactivatedMessage}
                        />
                    )}
                >
                    <ScraperForm endpoint={endpoint} data={scraper} method="PATCH" backURL={`/thinktank/${thinktankID}/`} />
                </Page>
            )}
        </Result>
    );
};

export default ScraperEdit;
