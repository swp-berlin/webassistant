import Page from 'components/Page';
import {useBreadcrumb} from 'components/Navigation';
import {PublicationPreview} from 'components/publication';

import _, {interpolate} from 'utils/i18n';
import {useQuery} from 'hooks/query';


const Loading = _('Loading');
const ThinktanksLabel = _('Thinktanks');
const PublicationsLabel = _('Publications');

const ThinktankPublications = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const {loading, result: {data: thinktank}} = useQuery(endpoint);
    const label = loading ? interpolate(_('Thinktank %s'), [id], false) : thinktank.name;

    useBreadcrumb('/thinktank/', ThinktanksLabel);
    useBreadcrumb(`/thinktank/${id}/`, label);
    useBreadcrumb(`/thinktank/${id}/publications/`, PublicationsLabel);

    if (loading) return Loading;

    return (
        <Page title={label} subtitle={thinktank.description}>
            <PublicationPreview thinktankID={+id} {...props} />
        </Page>
    );
};

export default ThinktankPublications;
