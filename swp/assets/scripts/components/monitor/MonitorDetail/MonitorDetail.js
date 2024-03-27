import {useCallback} from 'react';
import {Link, useParams} from 'react-router-dom';
import {Card} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {useQuery} from 'hooks/query';

import Page from 'components/Page';
import {Result} from 'components/Fetch';
import TableActions from 'components/tables/TableActions';
import {useMonitorsBreadcrumb} from 'components/monitor/MonitorList';

import {useMonitorBreadcrumb} from './hooks';

import MonitorActivationButton from './MonitorActivationButton';
import MonitorInfo from './MonitorInfo';
import TransferToZoteroButton from './TransferToZoteroButton';

const EditLabel = _('Edit');
const QueryLabel = _('Query');

const EditButton = ({id}) => (
    <Link to={`/monitor/${id}/edit/`} className="bp3-button bp3-icon-edit">
        {EditLabel}
    </Link>
);

const EditQueryButton = ({id}) => (
    <Link to={`/monitor/${id}/edit/query/`} className="bp3-button bp3-icon-edit bp3-small ml-2" />
);

const MonitorDetail = () => {
    const {id} = useParams();
    const endpoint = `/monitor/${id}/`;
    const result = useQuery(endpoint);
    const refetchMonitor = result.fetch;
    const handleMonitorUpdate = useCallback(() => refetchMonitor(), [refetchMonitor]);

    useMonitorsBreadcrumb();
    useMonitorBreadcrumb(endpoint, id, result.result.data);

    return (
        <Result result={result}>
            {({publication_count: publicationCount,
                new_publication_count: newPublicationCount,
                last_publication_count_update: lastPublicationCountUpdate,
                last_sent: lastSent,
                recipient_count: recipientCount,
                is_active: isActive,
                pool: {can_manage: canManage},
                name,
                description,
                interval,
                query,
            }) => (
                <Page
                    title={name}
                    actions={canManage && (
                        <MonitorActivationButton
                            endpoint={endpoint}
                            defaultIsActive={isActive}
                            onToggle={handleMonitorUpdate}
                        />
                    )}
                >
                    <p className="abstract mt-4">
                        {description}
                    </p>

                    <MonitorInfo
                        id={+id}
                        className="my-4"
                        canManage={canManage}
                        publicationCount={publicationCount}
                        newPublicationCount={newPublicationCount}
                        lastPublicationCountUpdate={lastPublicationCountUpdate}
                        lastSent={lastSent}
                        interval={interval}
                        recipientCount={recipientCount}
                        onMonitorUpdate={handleMonitorUpdate}
                    />

                    {canManage && (
                        <TableActions>
                            <EditButton id={id} />
                            <TransferToZoteroButton id={id} disabled={!isActive} />
                        </TableActions>
                    )}

                    <Card className="mt-2">
                        <div className="flex">
                            <h5>{QueryLabel}</h5>
                            {canManage && <EditQueryButton id={id} />}
                        </div>
                        <p className="my-2">{query}</p>
                    </Card>
                </Page>
            )}
        </Result>
    );
};

export default MonitorDetail;
