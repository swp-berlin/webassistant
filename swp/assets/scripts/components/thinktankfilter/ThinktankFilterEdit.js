import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';
import {useMonitorsBreadcrumb} from 'components/monitor/MonitorList';
import {useBreadcrumb} from 'components/Navigation';
import {Result} from 'components/Fetch';
import Page from 'components/Page';

import ThinktankFilterForm from './ThinktankFilterForm';


const Title = _('Edit Thinktank Filter');
const MonitorLabel = _('Monitor %s');
const SubmitButtonLabel = _('Save');

const getMonitorLabel = (id, {result: {data}, loading}) => (
    loading || !data ? interpolate(MonitorLabel, [id], false) : data.monitor.name
);

const ThinktankFilterEdit = ({monitorID, id}) => {
    const endpoint = `/thinktankfilter/${id}/`;
    const query = useQuery(endpoint);
    const monitorLabel = getMonitorLabel(monitorID, query);

    useMonitorsBreadcrumb();
    useBreadcrumb(`/monitor/${monitorID}/`, monitorLabel);
    useBreadcrumb(`/monitor/${monitorID}/filter/add/`, Title);

    return (
        <Result result={query}>
            {filter => (
                <Page title={Title}>
                    <ThinktankFilterForm
                        endpoint={`/thinktankfilter/${id}/`}
                        backURL={`/monitor/${monitorID}/`}
                        method="PATCH"
                        redirectURL={endpoint}
                        submitLabel={SubmitButtonLabel}
                        data={filter}
                    />
                </Page>
            )}
        </Result>
    );
};

export default ThinktankFilterEdit;
