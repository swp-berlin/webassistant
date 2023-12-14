import _ from 'utils/i18n';

import Page from 'components/Page';
import {useBreadcrumb} from 'components/Navigation';
import {useDefaultValues} from 'components/thinktank/ThinktankAddForm';

import MonitorForm, {DefaultValues} from './MonitorForm';
import {useMonitorsBreadcrumb} from './MonitorList';

const Title = _('New Monitor');
const SubmitLabel = _('Create');
const SuccessMessage = _('Successfully created monitor');

const MonitorAdd = props => {
    useMonitorsBreadcrumb();
    useBreadcrumb('/monitor/add/', Title);

    const defaultValues = useDefaultValues(DefaultValues);

    return (
        <Page title={Title}>
            <MonitorForm
                endpoint="/monitor/"
                method="POST"
                submitLabel={SubmitLabel}
                successMessage={SuccessMessage}
                defaultValues={defaultValues}
                backURL="/monitor/"
                {...props}
            />
        </Page>
    );
};

export default MonitorAdd;
