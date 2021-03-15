import classNames from 'classnames';

import PublicationItem from './PublicationItem';


const PublicationList = ({items, className, ...props}) => (
    <ul className={classNames('publication-list', 'list-none', 'space-y-4', 'p-0', items.length > 0 || 'empty', className)} {...props}>
        {items.map(publication => (
            <li key={publication.id}>
                <PublicationItem
                    id={publication.id}
                    title={publication.title}
                    subtitle={publication.subtitle}
                    tags={publication.tags}
                    authors={publication.authors}
                    abstract={publication.abstract}
                    publicationDate={publication.publication_date}
                    url={publication.url}
                    pdfURL={publication.pdf_url}
                    pdfPages={publication.pdf_pages}
                />
            </li>
        ))}
    </ul>
);

export default PublicationList;
