import {Callout} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {PublicationItem} from 'components/publication';

import {Status} from './common';


const ScrapingErrorText = _('Scraping failed with the following error:');


const getValues = (fields, errors) => ({
    title: errors.title || fields.title,
    authors: errors.author || [fields.author],
    abstract: errors.abstract || fields.abstract,
    publicationDate: errors.publication_date || fields.publication_date,
    pdfURL: errors.pdf_url || fields.pdf_url,
    pdfPages: fields.pdf_pages,
});


const PreviewResult = ({status, result: {success, error, publications}, traceback}) => {
    if (status === Status.Failure) {
        return <pre>{traceback}</pre>;
    }

    if (!success) {
        return (
            <Callout intent="danger" title="Scraper Error">
                <p>{ScrapingErrorText}</p>
                <pre className="mt-2 whitespace-pre-line">{error}</pre>
            </Callout>
        );
    }

    return (
        <ul className="list-none pl-0 space-y-8">
            {status === Status.Success && publications.map(({fields, errors}, idx) => (
                // eslint-disable-next-line react/no-array-index-key
                <li key={idx}>
                    <PublicationItem
                        id={idx}
                        {...getValues(fields, errors)}
                    />
                </li>
            ))}
        </ul>
    );
};

export default PreviewResult;
