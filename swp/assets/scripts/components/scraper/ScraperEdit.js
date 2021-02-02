import parseISO from 'date-fns/parseISO';
import format from 'date-fns/format';
import {de} from 'date-fns/locale';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faClock} from '@fortawesome/free-solid-svg-icons/faClock';

import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import ScraperForm from './ScraperForm';
import ScraperActivationButton from './ScraperActivationButton';


const Loading = _('Loading');
const ScraperLabel = _('Scraper');
const Thinktanks = _('Thinktanks');
const ThinktankLabel = _('Thinktank %s');

const LastRun = ({lastRun}) => (
    <div className="mt-2 flex items-center text-sm text-gray-500">
        <FontAwesomeIcon className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" icon={faClock} />
        {`Last run: ${format(parseISO(lastRun), 'PP pp', {locale: de})}`}
    </div>
);


const ScraperEdit = ({id, thinktankID}) => {
    const endpoint = `/scraper/${id}/`;
    const {loading, result: {data: scraper}} = useQuery(endpoint);

    const thinktankLabel = loading ? interpolate(ThinktankLabel, [thinktankID], false) : scraper.thinktank.name;

    useBreadcrumb('/thinktank/', Thinktanks);
    useBreadcrumb(`/thinktank/${thinktankID}/`, thinktankLabel);
    useBreadcrumb(endpoint, ScraperLabel);

    if (loading) return Loading;

    const {name, last_run: lastRun, is_active: isActive} = scraper;

    return (
        <Page
            title={name}
            subtitle={lastRun && <LastRun lastRun={lastRun} />}
            actions={<ScraperActivationButton id={id} initialIsActive={isActive} />}
        >
            <ScraperForm endpoint={endpoint} data={scraper} method="PATCH" redirectURL={`/thinktank/${thinktankID}/`} />
        </Page>
    );
};

export default ScraperEdit;
