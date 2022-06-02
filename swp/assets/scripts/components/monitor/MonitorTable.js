import {HTMLTable} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {useFetchHandler} from 'hooks/table';
import {useQuery} from 'hooks/query';

import {Result} from 'components/Fetch';
import {EmptyRow} from 'components/tables';

import MonitorRow from './MonitorRow';


const NameLabel = _('Name');
const RecipientsLabel = _('Recipients');
const PublicationsLabel = _('Publications');
const NewPublicationsLabel = _('New Publications');
const LastRunLabel = _('Last Run');


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

const MonitorTable = props => {
    const handler = useFetchHandler(5);
    const params = {ordering: 'name'};
    const query = useQuery('monitor', params);

    return (
        <HTMLTable className="thinktank-table w-full table-fixed my-4" bordered {...props}>
            <thead>
                <tr className="bg-gray-300">
                    <th className="w-1/2">{NameLabel}</th>
                    <th className="text-right">{RecipientsLabel}</th>
                    <th className="text-right">{PublicationsLabel}</th>
                    <th className="text-right">{NewPublicationsLabel}</th>
                    <th className="text-right">{LastRunLabel}</th>
                </tr>
            </thead>
            <tbody>
                <Result query={query} {...handler}>
                    {monitors => (
                        monitors.length ? <MonitorRows monitors={monitors} /> : <EmptyRow colSpan={5} />
                    )}
                </Result>
            </tbody>
        </HTMLTable>
    );
};

export default MonitorTable;
