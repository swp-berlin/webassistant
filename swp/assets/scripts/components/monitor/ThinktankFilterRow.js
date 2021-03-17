import {Link} from 'react-router-dom';

import MonitorPublicationsLink from './MonitorPublicationsLink';


const PublicationFilterItem = ({id, field, comparator, value}) => (
    <span className="publication-filter" data-id={id}>
        <span className="field">{field}</span>
        {' '}
        <span className="comparator">{comparator}</span>
        {' '}
        <q className="value">
            {value}
        </q>
    </span>
);

const PublicationFilters = ({filters}) => (
    <div className="flex flex-col">
        {filters.map(filter => <PublicationFilterItem key={filter.id} {...filter} />)}
    </div>
);


const ThinktankFilterRow = ({monitorID, id, name, filters, publicationCount, newPublicationCount}) => (
    <tr dataid={id}>
        <td><Link to={`/monitor/${monitorID}/filter/${id}/edit`}>{name || '—'}</Link></td>
        <td>{filters.length ? <PublicationFilters filters={filters} /> : '—'}</td>
        <td className="text-right">
            <MonitorPublicationsLink id={monitorID}>
                {publicationCount}
            </MonitorPublicationsLink>
        </td>
        <td className="text-right">
            <MonitorPublicationsLink id={monitorID} onlyNew>
                {newPublicationCount}
            </MonitorPublicationsLink>
        </td>
    </tr>
);

export default ThinktankFilterRow;
