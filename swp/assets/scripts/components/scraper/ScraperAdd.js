import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import ScraperForm from 'components/scraper/ScraperForm';


const Loading = _('Loading');
const Thinktanks = _('Thinktanks');
const NewScraperLabel = _('New Scraper');

const ScraperAdd = ({thinktankID}) => {
    const endpoint = `/thinktank/${thinktankID}/`;
    const {loading, result: {data: thinktank}} = useQuery(`/thinktank/${thinktankID}/`);

    const thinktankLabel = loading ? interpolate('Thinktank %s', [thinktankID], false) : thinktank.name;

    useBreadcrumb('/thinktank/', Thinktanks);
    useBreadcrumb(`/thinktank/${thinktankID}/`, thinktankLabel);
    useBreadcrumb(`/thinktank/${thinktankID}/scraper/add/`, NewScraperLabel);

    if (loading) return Loading;

    return (
        <Page title="Add Scraper">
            <ScraperForm endpoint={`/thinktank/${thinktankID}/add-scraper/`} redirectURL={endpoint} />
        </Page>
    );
};

export default ScraperAdd;
