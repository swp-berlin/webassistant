import {useCallback} from 'react';
import {Link} from 'react-router-dom';

import _ from 'utils/i18n';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import TableActions from 'components/tables/TableActions';
import Page from 'components/Page';
import {getMonitorLabel} from 'components/monitor/helper';
import {useMonitorsBreadcrumb} from 'components/monitor/MonitorList';
import {useUpdatePublicationsQuery} from 'hooks/publications';

import MonitorActivationButton from './MonitorActivationButton';
import MonitorInfo from './MonitorInfo';
import ThinktankFilterTable from './ThinktankFilterTable';
import TransferToZoteroButton from './TransferToZoteroButton';


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
    const refetchMonitor = result.fetch;
    const handleToggleActive = useCallback(() => refetchMonitor(), [refetchMonitor]);

    useMonitorsBreadcrumb();
    useBreadcrumb(endpoint, getMonitorLabel(id, result));

    return (
        <Result result={result}>
            {({publication_count: publicationCount,
                new_publication_count: newPublicationCount,
                last_publication_count_update: lastPublicationCountUpdate,
                transferred_count: transferredCount,
                last_sent: lastSent,
                recipient_count: recipientCount,
                is_active: isActive,
                name,
                description,
                interval,
                filters,
            }) => (
                <Page
                    title={name}
                    actions={(
                        <MonitorActivationButton
                            endpoint={endpoint}
                            defaultIsActive={isActive}
                            onToggle={handleToggleActive}
                        />
                    )}
                >
                    <p className="abstract mt-4">
                        {description}
                    </p>

                    <MonitorInfo
                        id={id}
                        className="my-4"
                        publicationCount={publicationCount}
                        newPublicationCount={newPublicationCount}
                        lastPublicationCountUpdate={lastPublicationCountUpdate}
                        transferredCount={transferredCount}
                        lastSent={lastSent}
                        interval={interval}
                        recipientCount={recipientCount}
                    />

                    <TableActions>
                        <EditButton id={id} />
                        <AddThinktankFilterButton id={id} />
                        <TransferToZoteroButton id={id} disabled={!isActive} />
                    </TableActions>

                    <ThinktankFilterTable items={filters} monitorID={id} />
                </Page>
            )}
        </Result>
    );
};

export default MonitorDetail;
