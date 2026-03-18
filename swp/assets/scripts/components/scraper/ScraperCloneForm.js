import Query from 'components/Query';

import ScraperForm from './ScraperForm';

export const ScraperCloneFormID = 'scraper-clone-form';

const ScraperCloneForm = ({scraperID, thinktankID, redirectURL, onSuccess}) => (
    <Query queryKey={['scraper', scraperID]}>
        {({id, ...scraper}) => (
            <ScraperForm
                key={id}
                id={ScraperCloneFormID}
                data={{...scraper, is_active: false}}
                redirectURL={redirectURL}
                onSuccess={onSuccess}
                endpoint={`/thinktank/${thinktankID}/add-scraper/`}
                hideSubmitButton
            />
        )}
    </Query>
);

export default ScraperCloneForm;
