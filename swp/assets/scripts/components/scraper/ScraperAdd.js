import {useQuery} from 'hooks/query';
import _ from 'utils/i18n';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import ScraperForm from 'components/scraper/ScraperForm';
import {getThinktankLabel} from 'components/thinktank/helper';
import {useParams} from 'react-router-dom';


const Title = _('Add Scraper');
const Thinktanks = _('Thinktanks');
const NewScraperLabel = _('New Scraper');

const ScraperAdd = () => {
    const {thinktankID} = useParams();
    const endpoint = `/thinktank/${thinktankID}/`;
    const result = useQuery(endpoint);
    const thinktankLabel = getThinktankLabel(thinktankID, result);

    useBreadcrumb('/thinktank/', Thinktanks);
    useBreadcrumb(`/thinktank/${thinktankID}/`, thinktankLabel);
    useBreadcrumb(`/thinktank/${thinktankID}/scraper/add/`, NewScraperLabel);

    return (
        <Result result={result}>
            {() => (
                <Page title={Title}>
                    <ScraperForm endpoint={`/thinktank/${thinktankID}/add-scraper/`} redirectURL={endpoint} />
                </Page>
            )}
        </Result>
    );
};

export default ScraperAdd;
