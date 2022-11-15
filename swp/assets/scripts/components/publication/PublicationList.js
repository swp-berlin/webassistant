import classNames from 'classnames';

import PublicationItem from './PublicationItem';

const getClassName = (items, className) => classNames(
    'publication-list',
    'list-none',
    'space-y-4',
    'p-0',
    className,
    {empty: items.length === 0},
);

const PublicationList = ({items, className, showMenu, ...props}) => (
    <ul className={getClassName(items, className)} {...props}>
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
                    doi={publication.doi}
                    isbn={publication.isbn}
                    url={publication.url}
                    pdfURL={publication.pdf_url}
                    pdfPages={publication.pdf_pages}
                    showMenu={showMenu}
                />
            </li>
        ))}
    </ul>
);

export default PublicationList;
