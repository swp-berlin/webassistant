import {forwardRef, cloneElement, useCallback, useEffect, useMemo, useState} from 'react';
import {Controller} from 'react-hook-form';
import {MenuItem} from '@blueprintjs/core';

import _ from 'utils/i18n';


const NoResultsLabel = _('No Results');

const DefaultItemRenderer = (item, {handleClick, modifiers: {active, disabled}}) => (
    <MenuItem
        key={item.value}
        text={item.label}
        onClick={handleClick}
        active={active}
        disabled={disabled}
    />
);

// eslint-disable-next-line no-unused-vars
const SelectController = forwardRef((props, ref) => {
    const {children, choices, onChange, value, itemRenderer, itemsEqual, onItemSelect, ...other} = props;
    const selected = useMemo(() => choices.find(choice => choice[itemsEqual] === value), [itemsEqual, choices, value]);
    const handleSelect = useCallback(item => {
        if (onChange) onChange(item[itemsEqual]);
        if (onItemSelect) onItemSelect(item);
    }, [onChange, itemsEqual, onItemSelect]);

    const [filteredItems, setFilteredItems] = useState(choices);
    const handleQueryChange = useCallback(
        query => setFilteredItems(choices.filter(item => item.label.toLowerCase().includes(query.toLowerCase()))),
        [choices],
    );

    useEffect(() => setFilteredItems(choices), [choices]);

    const selectProps = {
        activeItem: selected,
        value: selected,
        items: filteredItems,
        onQueryChange: handleQueryChange,
        inputValueRenderer: item => item.label,
        popoverProps: {fill: true},
        noResults: <MenuItem disabled active={false} text={NoResultsLabel} />,
        itemsEqual,
        itemRenderer,
        ...other,
        onItemSelect: handleSelect,
    };

    return cloneElement(children, selectProps);
});

SelectController.defaultProps = {
    itemRenderer: DefaultItemRenderer,
    itemsEqual: 'value',
};

export default ({as: InnerComponent, control, ...props}) => {
    if (control) {
        return (
            <Controller control={control} as={<SelectController><InnerComponent /></SelectController>} {...props} />
        );
    }

    return <SelectController {...props}><InnerComponent /></SelectController>;
};
