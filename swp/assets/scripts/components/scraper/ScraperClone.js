import Page from 'components/Page';

import _ from 'utils/i18n';

import {useQuery} from 'hooks/query';

import ScraperForm from './ScraperForm';

const Title = _('Clone Scraper');

const ScraperClone = ({endpoint, scraperID, thinktankID}) => {
    const query = useQuery(`/scraper/${scraperID}/`, {});
    const {loading, success, result: {data: scraper}} = query;
    if (success)
        scraper.id = 0;

    return (
        success ? (
            <Page title={Title}>
            <ScraperForm data={scraper} endpoint={`/thinktank/${thinktankID}/add-scraper/`}
                         redirectURL={endpoint} />
            </Page>
        ): loading ? (
            <Page title={Title}> loading... </Page>
        ): null

    )
}

export default ScraperClone;
