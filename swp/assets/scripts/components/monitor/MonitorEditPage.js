import {ClientError} from 'components/Fetch';
import Page from 'components/Page';

const MonitorEditPage = ({pool: {can_manage: canManage}, children, ...props}) => (
    <Page {...props}>
        {canManage ? children : <ClientError status={403} />}
    </Page>
);

export default MonitorEditPage;
