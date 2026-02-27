import {useState} from 'react';

import _ from 'utils/i18n';

import {useQuery} from 'hooks/query';

import Page from 'components/Page';

import {ScraperBaseForm} from './ScraperForm';

const Title = _('Clone Scraper');

const ScraperClone = ({endpoint, scraperID, thinktankID, onSuccess}) => {
    const query = useQuery(`/scraper/${scraperID}/`);
    const {loading, success, result: {data: scraper}} = query;
    const [isActive, setIsActive] = useState(!!scraper?.is_active);

    if (success)
        scraper.id = 0;

    return (
        success ?
            <Page title={Title}>
                <ScraperBaseForm
                    data={scraper}
                    redirectURL={endpoint}
                    onSuccess={onSuccess}
                    endpoint={`/thinktank/${thinktankID}/add-scraper/`}
                    isDisabled={isActive} onActivateToggle={setIsActive}
                />
            </Page>
        : loading ?
            <Page title={Title}> loading... </Page>
        : null
    )
}

export default ScraperClone;
