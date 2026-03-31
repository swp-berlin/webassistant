import {HTMLTable} from '@blueprintjs/core';

import _ from 'utils/i18n';

import EmptyRow from 'components/tables/EmptyRow';

import ScraperRow from './ScraperRow';

const URLLabel = _('URL');
const TypeLabel = _('Type');
const CategoriesLabel = _('Categories');
const LastRunLabel = _('Last Run');
const ErrorsLabel = _('Errors');
const Action = _('Action');

const ScraperRows = ({items, canManage}) => items.map(item => (
    <ScraperRow
        key={item.id}
        id={item.id}
        thinktankID={item.thinktank_id}
        url={item.start_url}
        type={item.type}
        categories={item.categories}
        lastRun={item.last_run}
        errorCount={item.error_count}
        isActive={item.is_active}
        isRunning={item.is_running}
        canManage={canManage}
    />
));

const ScraperTable = ({items, endpoint, canManage, ...props}) => (
    <HTMLTable className="w-full my-4 whitespace-nowrap" bordered {...props}>
        <thead>
            <tr className="bg-gray-300">
                <th className="w-1/2">{URLLabel}</th>
                <th>{TypeLabel}</th>
                <th>{CategoriesLabel}</th>
                <th>{LastRunLabel}</th>
                <th className="text-right">{ErrorsLabel}</th>
                <th>{Action}</th>
            </tr>
        </thead>
        <tbody>
            {items.length ? <ScraperRows items={items} canManage={canManage} /> : <EmptyRow colSpan={5} />}
        </tbody>
    </HTMLTable>
);

export default ScraperTable;
