import {Button, Intent} from '@blueprintjs/core';
import {Link} from 'react-router-dom';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _ from 'utils/i18n';

import MonitorTable from './MonitorTable';


const MonitorsLabel = _('Monitors');
const NewLabel = _('New Monitor');

export const useMonitorsBreadcrumb = (href = '/monitor/', text = MonitorsLabel) => (
    useBreadcrumb(href, text)
);

const MonitorAddButton = ({...props}) => (
    <Link to="/monitor/add/">
        <Button intent={Intent.PRIMARY} text={NewLabel} {...props} />
    </Link>
);

const MonitorList = () => {
    useBreadcrumb('/monitor/', MonitorsLabel);

    return (
        <Page title={MonitorsLabel} actions={<MonitorAddButton />}>
            <MonitorTable endpoint="monitor" />
        </Page>
    );
};

export default MonitorList;
