import {HTMLTable, Tooltip} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {getQueryComponents} from 'hooks/table';

import Query from 'components/Query';

import EmptyRow from './EmptyRow';
import ThinktankRow from './ThinktankRow';


const NameLabel = _('Name');
const PublicationsLabel = _('Publications');
const ScrapersLabel = _('Scrapers');
const LastRunLabel = _('Last Run');
const ErrorsLabel = _('Errors');

const ActiveTotalLabel = _('active / total');

const ColSpan = 5;

const QueryComponents = getQueryComponents(ColSpan);

const ThinktankRows = ({items}) => (
    items.map(thinktank => (
        <ThinktankRow
            key={thinktank.id}
            id={thinktank.id}
            name={thinktank.name}
            publicationCount={thinktank.publication_count}
            scraperCount={thinktank.scraper_count}
            activeScraperCount={thinktank.active_scraper_count}
            lastRun={thinktank.last_run}
            errorCount={thinktank.last_error_count}
            isActive={thinktank.is_active}
        />
    ))
);

const THR = ({children}) => <th className="text-right">{children}</th>;

const ThinktankTable = ({endpoint, pool, ...props}) => {
    const params = {ordering: 'name'};

    if (typeof pool === 'number') params.pool = pool;

    return (
        <HTMLTable className="thinktank-table w-full table-fixed my-4" bordered {...props}>
            <thead>
                <tr className="bg-gray-300">
                    <th className="w-1/2">{NameLabel}</th>
                    <THR>{PublicationsLabel}</THR>
                    <THR>
                        <Tooltip content={ActiveTotalLabel}>
                            {ScrapersLabel}
                        </Tooltip>
                    </THR>
                    <THR>{ErrorsLabel}</THR>
                    <THR>{LastRunLabel}</THR>
                </tr>
            </thead>
            <tbody>
                <Query queryKey={[endpoint, params]} components={QueryComponents}>
                    {items => items.length ? <ThinktankRows items={items} /> : <EmptyRow colSpan={ColSpan} />}
                </Query>
            </tbody>
        </HTMLTable>
    );
};

export default ThinktankTable;
