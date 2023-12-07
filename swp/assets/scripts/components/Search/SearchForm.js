import {useCallback} from 'react';
import {Button, Classes, ControlGroup} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {TextInput} from 'components/forms';

import DateRangePicker from './DateRangePicker';

const SearchLabel = _('Search');

const SearchForm = ({query, onQueryChange, initialDates, onDatesChange, onSearch}) => {
    const handleQueryChange = useCallback(event => onQueryChange(event.target.value), [onQueryChange]);
    const handleSubmit = useCallback(event => event.preventDefault() || onSearch(), [onSearch]);

    return (
        <form onSubmit={handleSubmit}>
            <ControlGroup fill className="mt-2">
                <TextInput
                    large
                    value={query}
                    onChange={handleQueryChange}
                    className="mb-0 h-8"
                    placeholder={SearchLabel}
                    rightElement={<DateRangePicker defaultValue={initialDates} onChange={onDatesChange} />}
                />
                <Button className={Classes.FIXED} large type="submit" disabled={query.length < 3}>{SearchLabel}</Button>
            </ControlGroup>
        </form>
    );
};

export default SearchForm;
