import TagCloud from './TagCloud';
import InteractiveTag from './InteractiveTag';

const sortAlphabetically = list => list.sort((a, b) => a.value.localeCompare(b.value));

const SearchResultTagCloud = ({label, values, selected, onSelect}) => (
    <TagCloud label={label}>
        {sortAlphabetically(values).map(({value, count}) => (
            <InteractiveTag
                key={value}
                value={value}
                label={`${value} (${count})`}
                selected={selected.includes(value)}
                onClick={onSelect}
            />
        ))}
    </TagCloud>
);

export default SearchResultTagCloud;
