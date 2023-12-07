import _ from 'utils/i18n';

import TagCloud from './TagCloud';
import InteractiveTag from './InteractiveTag';

const FilterByTagLabel = _('Filter by Tag:');

const sortAlphabetically = list => list.sort((a, b) => a.tag.localeCompare(b.tag));

const SearchResultTagCloud = ({tags, selected, onSelect}) => (
    <TagCloud label={FilterByTagLabel}>
        {sortAlphabetically(tags).map(({tag, count}) => (
            <InteractiveTag
                key={tag}
                value={tag}
                label={`${tag} (${count})`}
                selected={selected.includes(tag)}
                onClick={onSelect}
            />
        ))}
    </TagCloud>
);

export default SearchResultTagCloud;
