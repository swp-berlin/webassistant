import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _ from 'utils/i18n';
import {ThinktankAddForm} from './ThinktankForm';

const Title = _('New Thinktank');

const ThinktankAdd = ({...props}) => {
    useBreadcrumb('/thinktank/add/', Title);

    return (
        <Page title={Title}>
            <ThinktankAddForm
                endpoint="/thinktank/"
                redirectURL="/thinktank/"
                {...props}
            />
        </Page>
    );
};

export default ThinktankAdd;
