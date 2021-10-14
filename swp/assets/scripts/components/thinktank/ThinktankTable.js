import {HTMLTable, Tooltip} from '@blueprintjs/core';

import {useFetchHandler} from 'hooks/table';
import _ from 'utils/i18n';
import {Query} from 'components/Fetch';

import EmptyRow from './EmptyRow';
import ThinktankRow from './ThinktankRow';


const NameLabel = _('Name');
const PublicationsLabel = _('Publications');
const ScrapersLabel = _('Scrapers');
const LastRunLabel = _('Last Run');
const ErrorsLabel = _('Errors');

const ActiveTotalLabel = _('active / total');


const ThinktankRows = ({items}) => (
    [...items].sort((a, b) => a.name.localeCompare(b.name)).map(thinktank => (
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

const ThinktankTable = ({endpoint, ...props}) => {
    const handler = useFetchHandler(5);
    const params = {ordering: 'name'};
    return (
        <HTMLTable className="thinktank-table w-full table-fixed my-4" bordered {...props}>
            <thead>
                <tr className="bg-gray-300">
                    <th className="w-1/2">{NameLabel}</th>
                    <th className="text-right">{PublicationsLabel}</th>
                    <th className="text-right">
                        <Tooltip content={ActiveTotalLabel}>
                            {ScrapersLabel}
                        </Tooltip>
                    </th>
                    <th className="text-right">{ErrorsLabel}</th>
                    <th className="text-right">{LastRunLabel}</th>
                </tr>
            </thead>
            <tbody>
                <Query endpoint={endpoint || 'thinktank'} params={params} {...handler}>
                    {items => (
                        items.length ? <ThinktankRows items={items} /> : <EmptyRow colSpan={5} />
                    )}
                </Query>
            </tbody>
        </HTMLTable>
    );
};

export default ThinktankTable;
