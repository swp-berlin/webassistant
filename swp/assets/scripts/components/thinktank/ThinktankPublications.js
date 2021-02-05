import Page from 'components/Page';
import {useBreadcrumb} from 'components/Navigation';
import {PublicationPreview} from 'components/publication';

import {Result} from 'components/Fetch';
import {useQuery} from 'hooks/query';
import _ from 'utils/i18n';

import {getThinktankLabel} from './helper';

const ThinktanksLabel = _('Thinktanks');
const PublicationsLabel = _('Publications');

const ThinktankPublications = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const result = useQuery(endpoint);
    const label = getThinktankLabel(id, result);

    useBreadcrumb('/thinktank/', ThinktanksLabel);
    useBreadcrumb(`/thinktank/${id}/`, label);
    useBreadcrumb(`/thinktank/${id}/publications/`, PublicationsLabel);

    return (
        <Result result={result}>
            {
                ({description}) => (
                    <Page title={label} subtitle={description}>
                        <PublicationPreview thinktankID={+id} {...props} />
                    </Page>
                )
            }
        </Result>
    );
};

export default ThinktankPublications;
