import {useMemo} from 'react';
import {HTMLTable} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {Query} from 'components/Fetch';
import {
    handleLoading,
} from 'components/Fetch/defaultHandler';

import EmptyRow from './EmptyRow';
import ThinktankRow from './ThinktankRow';


const NameLabel = _('Name');
const PublicationsLabel = _('Publications');
const ScrapersLabel = _('Scrapers');
const LastRunLabel = _('Last Run');
const ErrorsLabel = _('Errors');


const useHandler = colSpan => useMemo(
    () => {
        const wrap = handler => (...args) => (
            <tr>
                <td colSpan={colSpan}>
                    {handler(...args)}
                </td>
            </tr>
        );

        return {
            handleLoading: wrap(handleLoading),
        };
    },
    [colSpan],
);

const ThinktankRows = ({items}) => (
    items.map(thinktank => (
        <ThinktankRow
            id={thinktank.id}
            name={thinktank.name}
            publicationCount={thinktank.publication_count}
            scraperCount={thinktank.scraper_count}
            lastRun={thinktank.last_run}
            errorCount={thinktank.last_error_count}
            isActive={thinktank.is_active}
        />
    ))
);

const ThinktankTable = ({endpoint, ...props}) => {
    const handler = useHandler(5);
    return (
        <HTMLTable className="w-full table-fixed my-4" bordered interactive {...props}>
            <thead>
                <tr className="bg-gray-300">
                    <th className="w-1/2">{NameLabel}</th>
                    <th>{PublicationsLabel}</th>
                    <th>{ScrapersLabel}</th>
                    <th>{LastRunLabel}</th>
                    <th>{ErrorsLabel}</th>
                </tr>
            </thead>
            <tbody>
                <Query endpoint={endpoint || 'thinktank'} {...handler}>
                    {items => (
                        items.length ? <ThinktankRows items={items} /> : <EmptyRow colSpan={5} />
                    )}
                </Query>
            </tbody>
        </HTMLTable>
    );
};

export default ThinktankTable;
