import {useParams} from 'react-router-dom';

import _ from 'utils/i18n';

import {useQuery} from 'hooks/query';

import {Result} from 'components/Fetch';

import {useMonitorsBreadcrumb} from './MonitorList';
import {useMonitorBreadcrumb} from './MonitorDetail';

import MonitorEditPage from './MonitorEditPage';
import MonitorForm from './MonitorForm';

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
                <MonitorEditPage pool={monitor.pool} title={Title}>
                    <MonitorForm
                        endpoint={endpoint}
                        method="PATCH"
                        submitLabel={SubmitLabel}
                        successMessage={SuccessMessage}
                        backURL={endpoint}
                        data={monitor}
                        {...props}
                    />
                </MonitorEditPage>
            )}
        </Result>
    );
};

export default MonitorEdit;
