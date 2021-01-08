import {useBreadcrumb} from 'components/Navigation';
import PageHeading from 'components/PageHeading';

import _ from 'utils/i18n';
import ThinktankForm from './ThinktankForm';

const Title = _('New Thinktank');
const SuccessMessage = _('Successfully created thinktank');

const NewThinktank = ({...props}) => {
    useBreadcrumb('/thinktank/new/', Title);

    return (
        <div>
            <PageHeading title={Title} />
            <ThinktankForm
                endpoint="/thinktank/"
                redirectURL="/thinktank/"
                successMessage={SuccessMessage}
                {...props}
            />
        </div>
    );
};

export default NewThinktank;
