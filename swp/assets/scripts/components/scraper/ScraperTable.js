import {HTMLTable} from '@blueprintjs/core';

import {useFetchHandler} from 'hooks/table';
import _ from 'utils/i18n';
import {Query} from 'components/Fetch';

import EmptyRow from 'components/tables/EmptyRow';
import ScraperRow from './ScraperRow';


const URLLabel = _('URL');
const TypeLabel = _('Type');
const LastRunLabel = _('Last Run');
const ErrorsLabel = _('Errors');

const ScraperRows = ({items}) => (
    items.length ? items.map(item => (
        <ScraperRow
            key={item.id}
            id={item.id}
            url={item.start_url}
            type={item.type}
            lastRun={item.last_run}
            errorCount={item.error_count}
            isActive={item.is_active}
        />
    )) : <EmptyRow colSpan={4} />
);

const ScraperTable = ({items, endpoint, ...props}) => {
    const handler = useFetchHandler(4);

    const rows = items ? <ScraperRows items={items} /> : (
        <Query endpoint={endpoint} {...handler}>
            {items => <ScraperRows items={items} />}
        </Query>
    );

    return (
        <HTMLTable className="w-full table-fixed my-4" bordered interactive {...props}>
            <thead>
                <tr className="bg-gray-300">
                    <th className="w-1/2">{URLLabel}</th>
                    <th>{TypeLabel}</th>
                    <th>{LastRunLabel}</th>
                    <th className="text-right">{ErrorsLabel}</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </HTMLTable>
    );
};

export default ScraperTable;
