import {useParams} from 'react-router-dom';

import _ from 'utils/i18n';

import {useQuery} from 'hooks/query';

import Page from 'components/Page';
import {Result} from 'components/Fetch';

import MonitorForm from './MonitorForm';
import {useMonitorsBreadcrumb} from './MonitorList';
import {useMonitorBreadcrumb} from './MonitorDetail';

const Title = _('Edit Monitor');
const SubmitLabel = _('Save');
const SuccessMessage = _('Successfully changed monitor');

const MonitorEdit = props => {
    const {id} = useParams();
    const endpoint = `/monitor/${id}/`;
    const result = useQuery(`/monitor/${id}/edit/`);

    useMonitorsBreadcrumb();
    useMonitorBreadcrumb(endpoint, id, result.result.data);

    return (
        <Result result={result}>
            {monitor => (
                <Page title={Title}>
                    <MonitorForm
                        endpoint={endpoint}
                        method="PATCH"
                        submitLabel={SubmitLabel}
                        successMessage={SuccessMessage}
                        backURL={endpoint}
                        data={monitor}
                        {...props}
                    />
                </Page>
            )}
        </Result>
    );
};

export default MonitorEdit;
