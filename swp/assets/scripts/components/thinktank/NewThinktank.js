import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _ from 'utils/i18n';
import ThinktankForm from './ThinktankForm';

const Title = _('New Thinktank');
const SuccessMessage = _('Successfully created thinktank');

const NewThinktank = ({...props}) => {
    useBreadcrumb('/thinktank/new/', Title);

    return (
        <Page title={Title}>
            <ThinktankForm
                endpoint="/thinktank/"
                redirectURL="/thinktank/"
                successMessage={SuccessMessage}
                {...props}
            />
        </Page>
    );
};

export default NewThinktank;
