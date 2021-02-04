import {Link} from 'react-router-dom';

import _ from 'utils/i18n';
import {useQuery} from 'hooks/query';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import TableActions from 'components/tables/TableActions';
import Page from 'components/Page';

import {getMonitorLabel} from './common';
import MonitorInfo from './MonitorInfo';
import FilterTable from './FilterTable';
import {useMonitorsBreadcrumb} from './MonitorList';


const EditLabel = _('Edit');
const AddThinktankLabel = _('Add Thinktank');

const EditButton = ({id}) => (
    <Link to={`/monitor/${id}/edit/`} className="bp3-button bp3-icon-edit">
        {EditLabel}
    </Link>
);

const AddThinktankButton = () => (
    <Link to="/thinktank/add/" className="bp3-button bp3-icon-add">
        {AddThinktankLabel}
    </Link>
);

const MonitorDetail = ({id}) => {
    const endpoint = `/monitor/${id}/`;
    const result = useQuery(endpoint);

    useMonitorsBreadcrumb();
    useBreadcrumb(endpoint, getMonitorLabel(id, result));

    return (
        <Result result={result}>
            {({publication_count: publicationCount,
                new_publication_count: newPublicationCount,
                last_sent: lastSent,
                recipient_count: recipientCount,
                name,
                interval,
                filters,
            }) => (
                <Page title={name} actions={<EditButton id={id} />}>
                    <MonitorInfo
                        className="my-4"
                        publicationCount={publicationCount}
                        newPublicationCount={newPublicationCount}
                        lastSent={lastSent}
                        interval={interval}
                        recipientCount={recipientCount}
                    />

                    <TableActions>
                        <AddThinktankButton />
                    </TableActions>

                    <FilterTable items={filters} />
                </Page>
            )}
        </Result>
    );
};

export default MonitorDetail;
