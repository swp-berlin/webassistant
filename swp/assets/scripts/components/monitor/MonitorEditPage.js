import {ClientError} from 'components/Fetch';
import Page from 'components/Page';

const MonitorEditPage = ({pool: {can_edit: canEdit}, children, ...props}) => (
    <Page {...props}>
        {canEdit ? children : <ClientError status={403} />}
    </Page>
);

export default MonitorEditPage;
