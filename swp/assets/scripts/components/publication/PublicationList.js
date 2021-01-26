import classNames from 'classnames';
import ExternalLink from 'components/Navigation/ExternalLink';
import CommaList from 'components/lists/CommaList';
import _, {interpolate} from 'utils/i18n';


const By = _('by');
const UnknownLabel = _('unkown');

const Authors = ({authors, className}) => (
    <span className={classNames('authors', authors.length || 'empty', className)}>
        {`${By} ` }
        {authors.length ? <CommaList items={authors} /> : UnknownLabel}
    </span>
);

const PublicationItem = ({id, title, authors, abstract, publicationDate, pdfURL, pdfPages, ...props}) => (
    <article className="publication-item mb-2" {...props}>
        <header>
            <h5>{title}</h5>
            <div className="subtitle">
                <Authors authors={authors} />
                <time className="ml-4">{publicationDate}</time>
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

const PublicationList = ({items, className, ...props}) => (
    <ul className={classNames('publication-list', 'list-none', 'p-0', items.length || 'empty', className)} {...props}>
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
