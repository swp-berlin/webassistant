import {Tag} from '@blueprintjs/core';
import {useLocation} from 'react-router-dom';

import _ from 'utils/i18n';

import {getPublicationsLabel, parsePageParam} from 'components/publication/helper';
import DownloadButton from 'components/publication/DownloadButton';
import PublicationResults from 'components/publication/PublicationResults';
import PublicationListMenu, {PublicationListDialog, QuickAddButton} from 'components/PublicationListMenu';

const NoPublicationsFound = _('No publications found');
const FilterByTagLabel = _('Filter by Tag:');

const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);
const sortAlphabetically = list => list.sort((a, b) => a.tag.localeCompare(b.tag));

const SearchResult = ({results, tags, next: nextPage, previous: prevPage, count, downloadURL, onSelectTag,
    onAddFilter}) => {

    const location = useLocation();
    const pageCount = calculatePageCount(count, 10);
    const currentPage = parsePageParam(location.search) || 1;
    const resultProps = {results, pageCount, currentPage, nextPage, prevPage, onAddFilter};

    return (
        <div className="publication-preview my-4">
            <header className="flex space-x-4 mb-2">
                <h3>{count ? getPublicationsLabel(count) : NoPublicationsFound}</h3>
                {count > 0 && <DownloadButton href={downloadURL} />}
            </header>

            {tags.length > 0 && (
                <div className="mt-2 mb-4 flex flex-wrap space-x-2">
                    <span>{FilterByTagLabel}</span>
                    {sortAlphabetically(tags).map(({tag, count}) => (
                        <Tag key={tag} interactive onClick={() => onSelectTag(tag)}>
                            {`+ ${tag} (${count})`}
                        </Tag>
                    ))}
                </div>
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
