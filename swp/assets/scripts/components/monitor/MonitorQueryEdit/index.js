import {useParams} from 'react-router-dom';

import _ from 'utils/i18n';

import {useQuery} from 'hooks/query';

import {Result} from 'components/Fetch';

import {useMonitorsBreadcrumb} from '../MonitorList';
import {useMonitorBreadcrumb} from '../MonitorDetail';

import MonitorEditPage from '../MonitorEditPage';
import MonitorQueryEditForm from './MonitorQueryEditForm';

const Title = _('Edit Query');

const MonitorQueryEdit = () => {
    const {id} = useParams();
    const endpoint = `/monitor/${id}/`;
    const result = useQuery(`/monitor/${id}/edit/`);

    useMonitorsBreadcrumb();
    useMonitorBreadcrumb(endpoint, id, result.result.data);

    return (
        <Result result={result}>
            {monitor => (
                <MonitorEditPage pool={monitor.pool} title={Title}>
                    <MonitorQueryEditForm endpoint={endpoint} monitor={monitor} />
                </MonitorEditPage>
            )}
        </Result>
    );
};

export default MonitorQueryEdit;
