import {useCallback} from 'react';
import {Button, ControlGroup} from '@blueprintjs/core';

import {TextInput} from 'components/forms';
import DateRangePicker from 'components/Search/DateRangePicker';
import _ from 'utils/i18n';

const SearchLabel = _('Search');

const SearchForm = ({query, onQueryChange, dates, onDatesChange, onSearch}) => {
    const handleQueryChange = useCallback(event => onQueryChange(event.target.value), [onQueryChange]);
    const handleSubmit = useCallback(event => event.preventDefault() || onSearch(), [onSearch]);

    return (
        <form onSubmit={handleSubmit}>
            <ControlGroup className="mt-2">
                <TextInput
                    value={query}
                    onChange={handleQueryChange}
                    className="mb-0 w-full"
                    placeholder={SearchLabel}
                    rightElement={<DateRangePicker defaultValue={dates} onChange={onDatesChange} />}
                />
                <Button className="h-8" type="submit" disabled={query.length < 3}>{SearchLabel}</Button>
            </ControlGroup>
        </form>
    );
};

export default SearchForm;
