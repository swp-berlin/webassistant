
const PublicationFilterItem = ({id, field, comparator, value}) => (
    <span className="publication-filter" dataid={id}>
        <span className="field">{field}</span>
        {' '}
        <span className="comparator">{comparator}</span>
        {' '}
        <q className="value">
            {value}
        </q>
    </span>
);

const PublicationFilters = ({filters}) => filters.map(
    filter => <PublicationFilterItem key={filter.id} {...filter} />,
);


const ThinktankFilterRow = ({id, name, filters, publicationCount, newPublicationCount}) => (
    <tr dataid={id}>
        <td>{name || '—'}</td>
        <td>{filters.length ? <PublicationFilters filters={filters} /> : '—'}</td>
        <td className="text-right">{publicationCount}</td>
        <td className="text-right">{newPublicationCount || 0}</td>
    </tr>
);

export default ThinktankFilterRow;
