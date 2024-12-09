import {useLocation} from 'react-router-dom';

import _ from 'utils/i18n';

import {parsePageParam} from 'components/publication/helper';
import DownloadButton from 'components/publication/DownloadButton';
import PublicationResults from 'components/publication/PublicationResults';
import PublicationListMenu, {PublicationListDialog, QuickAddButton} from 'components/PublicationListMenu';

import SearchResultTagCloud from './SearchResultTagCloud';
import SearchResultHeader from './SearchResultHeader';

const FilterByTagLabel = _('Filter by Tag:');
const FilterByCategoryLabel = _('Filter by Category:');

export const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);

const SearchResult = props => {
    const {
        query,
        results,
        tags,
        categories,
        selectedTags,
        selectedCategories,
        next: nextPage,
        previous: prevPage,
        count,
        downloadURL,
        onSelectTag,
        onSelectCategory,
        onAddFilter,
    } = props;
    const location = useLocation();
    const pageCount = calculatePageCount(count, 10);
    const currentPage = parsePageParam(location.search) || 1;
    const resultProps = {results, pageCount, currentPage, nextPage, prevPage, onAddFilter};

    return (
        <div className="publication-preview my-4">
            <SearchResultHeader query={query} count={count}>
                {count > 0 && <DownloadButton href={downloadURL} />}
            </SearchResultHeader>

            {categories.length > 0 && (
                <SearchResultTagCloud
                    label={FilterByCategoryLabel}
                    values={categories}
                    selected={selectedCategories}
                    onSelect={onSelectCategory}
                />
            )}

            {tags.length > 0 && (
                <SearchResultTagCloud
                    label={FilterByTagLabel}
                    values={tags}
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
