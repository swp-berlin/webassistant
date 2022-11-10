import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import {Result} from 'components/Fetch';
import {useMonitorsBreadcrumb} from 'components/monitor/MonitorList';

import ThinktankFilterForm from './ThinktankFilterForm';
import {useParams} from 'react-router-dom';


const Title = _('Add Thinktank Filter');
const MonitorLabel = _('Monitor %s');
const SubmitButtonLabel = _('Add');
const SuccessMessage = _('Successfully created filter');


const getMonitorLabel = (id, {result: {data}, loading}) => (
    loading || !data ? interpolate(MonitorLabel, [id], false) : data.name
);

const ThinktankFilterAdd = () => {
    const {id: monitorID} = useParams();
    const endpoint = `/monitor/${monitorID}/`;
    const query = useQuery(endpoint);
    const monitorLabel = getMonitorLabel(monitorID, query);

    useMonitorsBreadcrumb();
    useBreadcrumb(`/monitor/${monitorID}/`, monitorLabel);
    useBreadcrumb(`/monitor/${monitorID}/filter/add/`, Title);

    return (
        <Result result={query}>
            <Page title={Title}>
                <ThinktankFilterForm
                    endpoint={`/monitor/${monitorID}/add-filter/`}
                    backURL={`/monitor/${monitorID}/`}
                    redirectURL={endpoint}
                    submitLabel={SubmitButtonLabel}
                    successMessage={SuccessMessage}
                />
            </Page>
        </Result>
    );
};

export default ThinktankFilterAdd;
