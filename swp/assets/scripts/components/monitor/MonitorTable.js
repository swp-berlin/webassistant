import {HTMLTable} from '@blueprintjs/core';

import {useFetchHandler} from 'hooks/table';
import _ from 'utils/i18n';
import {Result} from 'components/Fetch';
import {EmptyRow} from 'components/tables';
import {useUpdatePublicationsQuery} from 'hooks/publications';

import MonitorRow from './MonitorRow';


const NameLabel = _('Name');
const RecipientsLabel = _('Recipients');
const PublicationsLabel = _('Publications');
const NewPublicationsLabel = _('New Publications');


const MonitorRows = ({monitors}) => (
    monitors.map(monitor => (
        <MonitorRow
            key={monitor.id}
            id={monitor.id}
            name={monitor.name}
            recipientCount={monitor.recipient_count}
            publicationCount={monitor.publication_count}
            newPublicationCount={monitor.new_publication_count}
        />
    ))
);

const ThinktankTable = ({endpoint, ...props}) => {
    const handler = useFetchHandler(5);
    const params = {ordering: 'name'};
    const query = useUpdatePublicationsQuery(endpoint || 'monitor', params);

    return (
        <HTMLTable className="thinktank-table w-full table-fixed my-4" bordered {...props}>
            <thead>
                <tr className="bg-gray-300">
                    <th className="w-1/2">{NameLabel}</th>
                    <th className="text-right">{RecipientsLabel}</th>
                    <th className="text-right">{PublicationsLabel}</th>
                    <th className="text-right">{NewPublicationsLabel}</th>
                </tr>
            </thead>
            <tbody>
                <Result query={query} {...handler}>
                    {monitors => (
                        monitors.length ? <MonitorRows monitors={monitors} /> : <EmptyRow colSpan={4} />
                    )}
                </Result>
            </tbody>
        </HTMLTable>
    );
};

export default ThinktankTable;
