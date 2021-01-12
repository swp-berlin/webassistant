import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';

import {ThinktankEditForm} from './ThinktankForm';


const Title = _('Edit Thinktank');
const Loading = _('Loading');

const getLabel = (id, loading, result) => {
    if (loading || !result) {
        return interpolate('Thinktank %s', [id], false);
    }

    return result.data.name;
};

const ThinktankEdit = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const {loading, result} = useQuery(endpoint);

    useBreadcrumb(`${endpoint}/edit/`, getLabel(id, loading, result));

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
