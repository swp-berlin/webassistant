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

const Fields = [
    'title',
    'subtitle',
    'tags',
    'authors',
    'abstract',
    'publication_date',
    'doi',
    'isbn',
    'url',
    'pdf_url',
    'pdf_pages',
];

const getPublication = ({fields, errors}, index) => {
    const publication = {id: index};

    Fields.forEach(field => {
        publication[field] = errors[field] || fields[field];
    });

    return publication;
};

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
            {status === Status.Success && result.publications.map(getPublication).map((publication, idx) => (
                <>
                    <li key={publication.id}>
                        <PublicationItem publication={publication} />
                    </li>
                    {isMultipage && maxPerPage - 1 === idx && <MultiPageMarker />}
                </>
            ))}
        </ul>
    );
};

export default PreviewResult;
