import {Link} from 'react-router-dom';

import ThinktankFilterPublicationsLink from 'components/thinktankfilter/ThinktankFilterPublicationsLink';


const PublicationFilterItem = ({id, field, comparator, values}) => (
    <span className="publication-filter" data-id={id}>
        <span className="field">{field}</span>
        {' '}
        <span className="comparator">{comparator}</span>
        {' '}
        {values.map(value => `"${value}"`).join(', ')}
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
            <ThinktankFilterPublicationsLink id={id} monitorID={monitorID}>
                {publicationCount}
            </ThinktankFilterPublicationsLink>
        </td>
        <td className="text-right">
            <ThinktankFilterPublicationsLink id={id} monitorID={monitorID} onlyNew>
                {newPublicationCount}
            </ThinktankFilterPublicationsLink>
        </td>
    </tr>
);

export default ThinktankFilterRow;
