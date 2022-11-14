import PublicationListEntry from './PublicationListEntry';

const PublicationList = ({publicationLists}) => (
    <ul className="publication-list">
        {publicationLists.map(publicationList => (
            <PublicationListEntry
                key={publicationList.id}
                {...publicationList}
            />
        ))}
    </ul>
);

export default PublicationList;
