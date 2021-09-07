import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _, {interpolate} from 'utils/i18n';
import {useQuery} from 'hooks/query';
import {Result} from 'components/Fetch';

import MonitorForm from './MonitorForm';
import {useMonitorsBreadcrumb} from './MonitorList';


const Title = _('Edit Monitor');
const MonitorLabel = _('Monitor %s');
const SubmitLabel = _('Save');
const SuccessMessage = _('Successfully changed monitor');


const getLabel = (id, {loading, result: {data}}) => {
    if (loading || !data) {
        return interpolate(MonitorLabel, [id], false);
    }

    return data.name;
};

const MonitorEdit = ({id, ...props}) => {
    const endpoint = `/monitor/${id}/`;
    const result = useQuery(endpoint);

    useMonitorsBreadcrumb();
    useBreadcrumb(endpoint, getLabel(id, result));

    return (
        <Result result={result}>
            {monitor => (
                <Page title={Title}>
                    <MonitorForm
                        endpoint={endpoint}
                        method="PATCH"
                        submitLabel={SubmitLabel}
                        successMessage={SuccessMessage}
                        backURL="/monitor/"
                        data={monitor}
                        {...props}
                    />
                </Page>
            )}
        </Result>
    );
};

export default MonitorEdit;
