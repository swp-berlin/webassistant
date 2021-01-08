import {useBreadcrumb} from 'components/Navigation';
import PageHeading from 'components/PageHeading';

import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';

import ThinktankForm from './ThinktankForm';


const Title = _('Edit Thinktank');
const Loading = _('Loading');
const SuccessMessage = _('Successfully changed thinktank');

const ThinktankEdit = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const {loading, result} = useQuery(endpoint);

    const label = interpolate('Thinktank %s', [id], false);
    useBreadcrumb(`${endpoint}/edit/`, label);

    if (loading) return Loading;
    const {data: thinktank} = result;

    return (
        <div>
            <PageHeading title={Title} />
            <ThinktankForm
                endpoint={endpoint}
                data={thinktank}
                redirectURL={endpoint}
                successMessage={SuccessMessage}
                {...props}
            />
        </div>
    );
};

export default ThinktankEdit;
