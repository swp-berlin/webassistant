import classNames from 'classnames';

import PublicationItem from './PublicationItem';


const PublicationList = ({items, className, ...props}) => (
    <ul
        className={classNames('publication-list', 'list-none', 'p-0', items.length > 0 || 'empty', className)}
        {...props}
    >
        {items.map(publication => (
            <li key={publication.id}>
                <PublicationItem
                    id={publication.id}
                    title={publication.title}
                    authors={publication.authors}
                    abstract={publication.abstract}
                    publicationDate={publication.publication_date}
                    pdfURL={publication.pdf_url}
                    pdfPages={publication.pdf_pages}
                />
            </li>
        ))}
    </ul>
);

export default PublicationList;
