import classNames from 'classnames';
import {Icon} from '@blueprintjs/core';
import ExternalLink from 'components/Navigation/ExternalLink';
import CommaList from 'components/lists/CommaList';
import _, {interpolate} from 'utils/i18n';


const By = _('by');
const UnknownLabel = _('unknown');
const PagesLabel = _('%s pages');
const PDFNotFoundLabel = _('No PDF found');

const Authors = ({authors, className}) => (
    <span className={classNames('authors', {empty: authors.length === 0}, className)}>
        {`${By} ` }
        {authors.length ? <CommaList items={authors} /> : UnknownLabel}
    </span>
);

const PDFNotFound = () => (
    <span className="text-gray-500">
        <Icon className="mr-1" icon="issue" />
        {PDFNotFoundLabel}
    </span>
);

export const PublicationItem = ({id, title, authors, abstract, publicationDate, url, pdfURL, pdfPages, ...props}) => (
    <article className="publication-item mb-2" {...props}>
        <header>
            <h5>{url ? <a href={url}>{title}</a> : title}</h5>
            <div className="subtitle">
                <Authors authors={authors} />
                <time className="ml-4">{publicationDate}</time>
            </div>
        </header>
        <p className="abstract my-2">
            {abstract}
        </p>
        <footer>
            {pdfURL ? <ExternalLink to={pdfURL} /> : <PDFNotFound />}
            {pdfPages > 0 && <span className="ml-2 text-gray-500">{interpolate(PagesLabel, [pdfPages], false)}</span>}
        </footer>
    </article>
);

const PublicationList = ({items, className, ...props}) => (
    <ul className={classNames('publication-list', 'list-none', 'space-y-4', 'p-0', items.length > 0 || 'empty', className)} {...props}>
        {items.map(publication => (
            <li key={publication.id}>
                <PublicationItem
                    id={publication.id}
                    title={publication.title}
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
