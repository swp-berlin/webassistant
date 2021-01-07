import {Button} from '@blueprintjs/core';
import parseISO from 'date-fns/parseISO';
import format from 'date-fns/format';
import {de} from 'date-fns/locale';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faClock} from '@fortawesome/free-solid-svg-icons/faClock';

import {useQuery} from 'hooks/query';
import {interpolate} from 'utils/i18n';
import {useBreadcrumb} from 'components/Navigation';
import PageHeading from 'components/PageHeading';
import ScraperForm from 'components/scraper/ScraperForm';


const LastRun = ({lastRun}) => (
    <div className="mt-2 flex items-center text-sm text-gray-500">
        <FontAwesomeIcon className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" icon={faClock} />
        {`Last run: ${format(parseISO(lastRun), 'PP pp', {locale: de})}`}
    </div>
);


const Scraper = ({id}) => {
    const {loading, result} = useQuery(`/scraper/${id}/`);

    const label = interpolate('Scraper %s', [id], false);
    useBreadcrumb(`/scraper/${id}`, label);

    if (loading) return 'Loading';

    const {data: scraper} = result;
    const {thinktank, last_run: lastRun, is_active: isActive} = scraper;

    return (
        <div>
            <PageHeading
                title={`${thinktank.name} Scraper`}
                subtitle={lastRun && <LastRun lastRun={lastRun} />}
                actions={[<Button key="disable" intent="primary" text={isActive ? 'Disable' : 'Enable'} />]}
            />
            <ScraperForm id={id} data={scraper} />
        </div>
    );
};

export default Scraper;
