import {Button} from '@blueprintjs/core';
import parseISO from 'date-fns/parseISO';
import format from 'date-fns/format';
import {de} from 'date-fns/locale';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faClock} from '@fortawesome/free-solid-svg-icons/faClock';

import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import ScraperForm from 'components/scraper/ScraperForm';


const Loading = _('Loading');
const Thinktanks = _('Thinktanks');

const LastRun = ({lastRun}) => (
    <div className="mt-2 flex items-center text-sm text-gray-500">
        <FontAwesomeIcon className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" icon={faClock} />
        {`Last run: ${format(parseISO(lastRun), 'PP pp', {locale: de})}`}
    </div>
);


const ScraperDetail = ({id, thinktankID}) => {
    const endpoint = `/scraper/${id}/`;
    const {loading, result: {data: scraper}} = useQuery(endpoint);

    const label = loading ? interpolate('Scraper %s', [id], false) : scraper.name;
    const thinktankLabel = loading ? interpolate('Thinktank %s', [thinktankID], false) : scraper.thinktank.name;

    useBreadcrumb('/thinktank/', Thinktanks);
    useBreadcrumb(`/thinktank/${thinktankID}/`, thinktankLabel);
    useBreadcrumb(endpoint, label);

    if (loading) return Loading;

    const {name, last_run: lastRun, is_active: isActive} = scraper;

    return (
        <Page
            title={name}
            subtitle={lastRun && <LastRun lastRun={lastRun} />}
            actions={<Button intent="primary" text={isActive ? 'Disable' : 'Enable'} />}
        >
            <ScraperForm id={id} data={scraper} />
        </Page>
    );
};

export default ScraperDetail;
