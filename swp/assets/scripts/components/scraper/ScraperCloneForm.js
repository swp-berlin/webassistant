import {useState} from 'react';

import {useQuery} from 'hooks/query';

import {Result} from 'components/Fetch';

import {ScraperBaseForm} from './ScraperForm';

export const ScraperCloneFormID = 'scrapercloneform';


const ScraperCloneForm = ({endpoint, scraperID, thinktankID, onSuccess}) => {
    const [isActive, setIsActive] = useState();
    // eslint-disable-next-line no-param-reassign
    const query = useQuery(`scraper/${scraperID}`, onSuccess = scraper => setIsActive(scraper?.is_active));

    return (
        <Result result={query}>
            {scraper => {
                scraper.id = 0;

                return (
                    <ScraperBaseForm
                        id={ScraperCloneFormID}
                        data={scraper}
                        redirectURL={endpoint}
                        onSuccess={onSuccess}
                        endpoint={`/thinktank/${thinktankID}/add-scraper/`}
                        isDisabled={isActive}
                        onActivateToggle={setIsActive}
                    />
                );
            }}
        </Result>
    );
};

export default ScraperCloneForm;
