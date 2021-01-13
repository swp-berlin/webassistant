import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _ from 'utils/i18n';
import ThinktankAddForm from './ThinktankAddForm';
import {useThinktanksBreadcrumb} from './ThinktankList';


const Title = _('New Thinktank');

const ThinktankAdd = ({...props}) => {
    useThinktanksBreadcrumb();
    useBreadcrumb('/thinktank/add/', Title);

    return (
        <Page title={Title}>
            <ThinktankAddForm
                endpoint="/thinktank/"
                backURL="/thinktank/"
                {...props}
            />
        </Page>
    );
};

export default ThinktankAdd;
