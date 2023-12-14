import {useLocation} from 'react-router-dom';

import {parsePageParam} from 'components/publication/helper';
import DownloadButton from 'components/publication/DownloadButton';
import PublicationResults from 'components/publication/PublicationResults';
import PublicationListMenu, {PublicationListDialog, QuickAddButton} from 'components/PublicationListMenu';

import SearchResultTagCloud from './SearchResultTagCloud';
import SearchResultHeader from './SearchResultHeader';

export const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);

const SearchResult = ({
    results, tags, selectedTags, next: nextPage, previous: prevPage, count, downloadURL, onSelectTag, onAddFilter,
}) => {

    const location = useLocation();
    const pageCount = calculatePageCount(count, 10);
    const currentPage = parsePageParam(location.search) || 1;
    const resultProps = {results, pageCount, currentPage, nextPage, prevPage, onAddFilter};

    return (
        <div className="publication-preview my-4">
            <SearchResultHeader count={count}>
                {count > 0 && <DownloadButton href={downloadURL} />}
            </SearchResultHeader>

            {tags.length > 0 && (
                <SearchResultTagCloud
                    tags={tags}
                    selected={selectedTags}
                    onSelect={onSelectTag}
                />
            )}

            {count > 0 && (
                <PublicationResults {...resultProps}>
                    <PublicationListMenu>
                        <PublicationListDialog />
                        <QuickAddButton />
                    </PublicationListMenu>
                </PublicationResults>
            )}
        </div>
    );
};

export default SearchResult;
