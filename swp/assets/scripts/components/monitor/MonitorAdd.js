import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _ from 'utils/i18n';
import MonitorForm from './MonitorForm';
import {useMonitorsBreadcrumb} from './MonitorList';


const Title = _('New Monitor');
const SubmitLabel = _('Create');
const SuccessMessage = _('Successfully created monitor');

const MonitorAdd = props => {
    useMonitorsBreadcrumb();
    useBreadcrumb('/monitor/add/', Title);

    return (
        <Page title={Title}>
            <MonitorForm
                endpoint="/monitor/"
                method="POST"
                submitLabel={SubmitLabel}
                successMessage={SuccessMessage}
                backURL="/monitor/"
                {...props}
            />
        </Page>
    );
};

export default MonitorAdd;
