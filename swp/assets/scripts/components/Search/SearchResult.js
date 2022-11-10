import {getPublicationsLabel, parsePageParam} from 'components/publication/helper';
import DownloadButton from 'components/publication/DownloadButton';
import {Tag} from '@blueprintjs/core';
import PublicationResults from 'components/publication/PublicationResults';
import {useLocation} from 'react-router-dom';
import _ from 'utils/i18n';

const NoPublicationsFound = _('No publications found');
const FilterByTagLabel = _('Filter by Tag');

const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);


const SearchResult = ({results, tags, next: nextPage, previous: prevPage, count, downloadURL, onSelectTag}) => {
    const location = useLocation();
    const currentPage = parsePageParam(location.search) || 1;

    return (
        <div className="publication-preview my-4">
            <header className="flex space-x-4 mb-2">
                <h3>{count ? getPublicationsLabel(count) : NoPublicationsFound}</h3>
                {count > 0 && <DownloadButton href={downloadURL} />}
            </header>

            {tags.length > 0 && (
                <div className="mt-2 mb-4 flex flex-wrap space-x-2">
                    <span>{FilterByTagLabel}:</span>
                    {tags.map(({tag, count}) => (
                        <Tag key={tag} interactive onClick={() => onSelectTag(tag)}>{`${tag} (${count})`}</Tag>
                    ))}
                </div>
            )}

            {count > 0 && (
                <PublicationResults
                    results={results}
                    pageCount={calculatePageCount(count, 10)}
                    currentPage={currentPage}
                    nextPage={nextPage}
                    prevPage={prevPage}
                />
            )}
        </div>
    );
};

export default SearchResult;
