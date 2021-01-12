import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';

import {ThinktankEditForm} from './ThinktankForm';


const Title = _('Edit Thinktank');
const Loading = _('Loading');

const ThinktankEdit = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const {loading, result} = useQuery(endpoint);

    const label = loading ? interpolate('Thinktank %s', [id], false) : result.data.name;
    useBreadcrumb(`${endpoint}/edit/`, label);

    if (loading) return Loading;
    const {data: thinktank} = result;

    return (
        <Page title={Title}>
            <ThinktankEditForm
                endpoint={endpoint}
                data={thinktank}
                redirectURL={endpoint}
                {...props}
            />
        </Page>
    );
};

export default ThinktankEdit;
