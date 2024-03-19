import {HTMLTable} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {getQueryComponents} from 'hooks/table';

import {EmptyRow, THR} from 'components/tables';
import Query from 'components/Query';

import MonitorRow from './MonitorRow';

const NameLabel = _('Name');
const RecipientsLabel = _('Recipients');
const PublicationsLabel = _('Publications');
const NewPublicationsLabel = _('New Publications');
const LastRunLabel = _('Last Run');

const ColSpan = 5;

const QueryComponents = getQueryComponents(ColSpan);

const MonitorRows = ({monitors}) => (
    monitors.map(monitor => (
        <MonitorRow
            key={monitor.id}
            id={monitor.id}
            name={monitor.name}
            recipientCount={monitor.recipient_count}
            publicationCount={monitor.publication_count}
            newPublicationCount={monitor.new_publication_count}
            lastSent={monitor.last_sent}
            isActive={monitor.is_active}
        />
    ))
);

const MonitorTable = ({pool, ...props}) => {
    const params = {ordering: 'name'};

    if (typeof pool === 'number') params.pool = pool;

    return (
        <HTMLTable className="thinktank-table w-full table-fixed my-4" bordered {...props}>
            <thead>
                <tr className="bg-gray-300">
                    <th className="w-1/2">{NameLabel}</th>
                    <THR>{RecipientsLabel}</THR>
                    <THR>{PublicationsLabel}</THR>
                    <THR>{NewPublicationsLabel}</THR>
                    <THR>{LastRunLabel}</THR>
                </tr>
            </thead>
            <tbody>
                <Query queryKey={['monitor', params]} components={QueryComponents}>
                    {monitors => monitors.length ? <MonitorRows monitors={monitors} /> : <EmptyRow colSpan={ColSpan} />}
                </Query>
            </tbody>
        </HTMLTable>
    );
};

export default MonitorTable;
