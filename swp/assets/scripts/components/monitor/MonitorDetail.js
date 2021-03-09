import {Link} from 'react-router-dom';

import _ from 'utils/i18n';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import TableActions from 'components/tables/TableActions';
import Page from 'components/Page';
import {useUpdatePublicationsQuery} from 'hooks/publications';

import {getMonitorLabel} from './helper';
import MonitorInfo from './MonitorInfo';
import {useMonitorsBreadcrumb} from './MonitorList';
import ThinktankFilterTable from './ThinktankFilterTable';


const EditLabel = _('Edit');
const AddThinktankLabel = _('Add Thinktank');

const EditButton = ({id}) => (
    <Link to={`/monitor/${id}/edit/`} className="bp3-button bp3-icon-edit">
        {EditLabel}
    </Link>
);

const AddThinktankFilterButton = ({id}) => (
    <Link to={`/monitor/${id}/filter/add/`} className="bp3-button bp3-icon-add">
        {AddThinktankLabel}
    </Link>
);

const MonitorDetail = ({id}) => {
    const endpoint = `/monitor/${id}/`;
    const result = useUpdatePublicationsQuery(endpoint);

    useMonitorsBreadcrumb();
    useBreadcrumb(endpoint, getMonitorLabel(id, result));

    return (
        <Result result={result}>
            {({publication_count: publicationCount,
                new_publication_count: newPublicationCount,
                last_sent: lastSent,
                recipient_count: recipientCount,
                name,
                description,
                interval,
                filters,
            }) => (
                <Page title={name} actions={<EditButton id={id} />}>
                    <p className="abstract mt-4">
                        {description}
                    </p>

                    <MonitorInfo
                        id={id}
                        className="my-4"
                        publicationCount={publicationCount}
                        newPublicationCount={newPublicationCount}
                        lastSent={lastSent}
                        interval={interval}
                        recipientCount={recipientCount}
                    />

                    <TableActions>
                        <AddThinktankFilterButton id={id} />
                    </TableActions>

                    <ThinktankFilterTable items={filters} monitorID={id} />
                </Page>
            )}
        </Result>
    );
};

export default MonitorDetail;
