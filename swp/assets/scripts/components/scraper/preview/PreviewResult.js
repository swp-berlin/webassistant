import _ from 'utils/i18n';
import {PublicationItem} from 'components/publication';

import {Status} from './common';
import PreviewError from './PreviewError';


const InternalErrorText = _('Internal Error');
const MultiPageLabel = _('Continued from page 2');


const MultiPageMarker = () => (
    <div>
        <hr className="mb-4" />
        <span>{MultiPageLabel}</span>
    </div>
);

const getValues = (fields, errors) => ({
    title: errors.title || fields.title,
    authors: errors.authors || fields.authors,
    abstract: errors.abstract || fields.abstract,
    publicationDate: errors.publication_date || fields.publication_date,
    url: errors.url || fields.url,
    pdfURL: errors.pdf_url || fields.pdf_url,
    pdfPages: fields.pdf_pages,
});


// NOTE `result` refers to the response body, as the return value from `useQuery` gets shadowed.
const PreviewResult = ({status, result, traceback}) => {
    if (status === Status.Failure) {
        console.log(traceback); // eslint-disable-line no-console
        return <PreviewError error={InternalErrorText} />;
    }

    if (!result.success) {
        return <PreviewError error={result.error} />;
    }

    const {is_multipage: isMultipage, max_per_page: maxPerPage} = result;

    return (
        <ul className="list-none pl-0 space-y-8">
            {status === Status.Success && result.publications.map(({fields, errors}, idx) => (
                <>
                    <li key={idx /* eslint-disable-line react/no-array-index-key */}>
                        <PublicationItem
                            id={idx}
                            {...getValues(fields, errors)}
                        />
                    </li>
                    {isMultipage && maxPerPage - 1 === idx && <MultiPageMarker />}
                </>
            ))}
        </ul>
    );
};

export default PreviewResult;
