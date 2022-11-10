import {useParams} from 'react-router-dom';

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
const SuccessMessage = _('Successfully changed filter');

const getMonitorLabel = (id, {result: {data}, loading}) => (
    loading || !data ? interpolate(MonitorLabel, [id], false) : data.monitor.name
);

const ThinktankFilterEdit = () => {
    const {monitorID, id} = useParams();
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
                        redirectURL={`/monitor/${monitorID}/`}
                        submitLabel={SubmitButtonLabel}
                        successMessage={SuccessMessage}
                        data={filter}
                    />
                </Page>
            )}
        </Result>
    );
};

export default ThinktankFilterEdit;
