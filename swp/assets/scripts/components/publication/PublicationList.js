import ExternalLink from 'components/Navigation/ExternalLink';
import {interpolate} from 'utils/i18n';


const Authors = ({authors}) => (
    <ul className="inline list-inline">
        {authors.map((author, i) => <li key={author}>{i > 0 ? `, ${author}` : author}</li>)}
    </ul>
);

const PublicationItem = ({id, title, authors, abstract, publicationDate, pdfURL, pdfPages, ...props}) => (
    <article className="publication-item mb-2" {...props}>
        <header>
            <h4>{title}</h4>
            <div className="subtitle">
                <span>by </span>
                <Authors authors={authors} />
                <time>{publicationDate}</time>
            </div>
        </header>
        <p className="abstract my-2">
            {abstract}
        </p>
        <footer className="flex justify-between">
            <ExternalLink to={pdfURL} />
            <span>{interpolate('%s pages', [pdfPages], false)}</span>
        </footer>
    </article>
);

const PublicationList = ({items, ...props}) => (
    <ul className="list-none p-0" {...props}>
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
