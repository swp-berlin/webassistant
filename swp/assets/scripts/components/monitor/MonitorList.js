import {Button, Intent} from '@blueprintjs/core';
import {Link} from 'react-router-dom';

import _ from 'utils/i18n';
import {buildURL, withParams} from 'utils/url';

import Page from 'components/Page';
import {useBreadcrumb} from 'components/Navigation';
import {usePoolSelect} from 'components/PoolSelect';

import MonitorTable from './MonitorTable';

const MonitorsLabel = _('Monitors');
const NewLabel = _('New Monitor');

export const useMonitorsBreadcrumb = (href = '/monitor/', text = MonitorsLabel) => (
    useBreadcrumb(href, text)
);

const MonitorAddURL = buildURL('monitor', 'add');

const getAddURL = pool => typeof pool === 'number' ? withParams(MonitorAddURL, {pool}) : MonitorAddURL;

const MonitorAddButton = ({pool, ...props}) => (
    <Link to={getAddURL(pool)}>
        <Button intent={Intent.PRIMARY} text={NewLabel} {...props} />
    </Link>
);

const MonitorList = () => {
    useMonitorsBreadcrumb();

    const [pool, poolSelect] = usePoolSelect();
    const actions = (
        <>
            {poolSelect}
            <MonitorAddButton pool={pool} />
        </>
    );

    return (
        <Page title={MonitorsLabel} actions={actions}>
            <MonitorTable pool={pool} />
        </Page>
    );
};

export default MonitorList;
