import {cloneElement} from 'react';
import {Icon} from '@blueprintjs/core';
import classNames from 'classnames';

import _, {interpolate} from 'utils/i18n';

import PublicationField from 'components/publication/PublicationField';
import ExternalLink from 'components/Navigation/ExternalLink';
import CommaList from 'components/lists/CommaList';


const By = _('by');
const UnknownLabel = _('unknown');
const ISBNLabel = _('ISBN: %s');
const PagesLabel = _('%s pages');
const PDFNotFoundLabel = _('No PDF found');


const Authors = ({authors, className, onFilter}) => (
    <span className={classNames('authors', {empty: !authors?.length}, className)}>
        {`${By} ` }
        {authors?.length ? (
            <CommaList
                inline
                items={authors.map(author => <Filterable field="authors" text={author} onFilter={onFilter} />)}
            />
        ) : UnknownLabel}
    </span>
);

const PDFNotFound = () => (
    <span className="text-gray-500">
        <Icon className="mr-1" icon="issue" />
        {PDFNotFoundLabel}
    </span>
);

const Filterable = ({field, text, value, onFilter, className, ...props}) => {
    if (!onFilter) return text;

    return (
        <span
            onClick={() => onFilter({field, value: value || text})}
            onKeyDown={event => event.key === 'Enter' && onFilter({field, value: value || text})}
            role="link"
            tabIndex="0"
            className={classNames('hover:underline hover:cursor-pointer', className)}
            {...props}
        >
            {text}
        </span>
    );
};

const PublicationItem = ({publication, className, onAddFilter, children, ...props}) => {
    const {
        id,
        thinktank_id: thinktankID,
        thinktank_name: thinktankName,
        title,
        subtitle,
        tags,
        authors,
        abstract,
        publication_date: publicationDate,
        doi,
        isbn,
        url,
        pdf_url: pdfURL,
        pdf_pages: pdfPages,
    } = publication;

    return (
        <article className={classNames('publication-item', className, 'relative')} data-id={id} {...props}>
            <header>
                <h5>
                    <PublicationField name="title" value={title}>
                        {url ? <a href={url}>{title}</a> : title}
                    </PublicationField>
                </h5>
                <h6 className="italic mb-2 text-sm text-gray-800">
                    <Filterable field="thinktank.id" text={thinktankName} value={thinktankID} onFilter={onAddFilter} />
                </h6>
                <div className="subtitle">
                    {subtitle && (
                        <PublicationField name="subtitle" value={subtitle}>
                            <h6 className="italic mb-2 text-base text-gray-800">
                                {subtitle}
                            </h6>
                        </PublicationField>
                    )}
                    <PublicationField name="author" value={authors}>
                        <Authors authors={authors} onFilter={onAddFilter} />
                    </PublicationField>
                    <PublicationField name="publication_date" value={publicationDate}>
                        <time className="ml-4">{publicationDate}</time>
                    </PublicationField>
                    {doi && (
                        <PublicationField name="doi" value={doi}>
                            <p>{doi}</p>
                        </PublicationField>
                    )}
                    {isbn && (
                        <PublicationField name="isbn" value={isbn}>
                            <p>{interpolate(ISBNLabel, [isbn], false)}</p>
                        </PublicationField>
                    )}
                </div>
            </header>
            <PublicationField name="abstract" className="min-h-100 flex items-center" value={abstract}>
                <p className="abstract my-2">
                    {abstract}
                </p>
            </PublicationField>
            <footer>
                {tags && (
                    <PublicationField name="tags" value={tags}>
                        <CommaList
                            className="italic text-gray-400"
                            items={tags.map(tag => <Filterable field="tags" text={tag} onFilter={onAddFilter} />)}
                            conjunction=","
                        />
                    </PublicationField>
                )}
                {pdfURL ? (
                    <PublicationField name="pdf_url" value={pdfURL}><ExternalLink to={pdfURL} /></PublicationField>
                ) : <PDFNotFound />}
                {pdfPages > 0 && (
                    <span className="ml-2 text-gray-500">{interpolate(PagesLabel, [pdfPages], false)}</span>
                )}
            </footer>
            {children && cloneElement(children, {publication})}
        </article>
    );
};

export default PublicationItem;
