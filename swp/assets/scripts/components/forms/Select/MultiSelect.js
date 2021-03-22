import {useCallback, useMemo} from 'react';
import {useController} from 'react-hook-form';
import {MenuItem} from '@blueprintjs/core';
import {MultiSelect as BPMultiSelect} from '@blueprintjs/select';
import keyBy from 'lodash/keyBy';

import Field from '../Field';


const Item = ({item, handleClick, modifiers: {active, disabled}, selected}) => (
    <MenuItem
        text={item.label}
        icon={selected ? 'tick' : 'blank'}
        onClick={handleClick}
        active={active}
        disabled={disabled}
    />
);

const TagRenderer = ({label}) => label;

const tagInputProps = {inputProps: {onKeyPress: e => e.key === 'Enter' && e.preventDefault()}};

const useMapChoicesToItems = ({choices, values, valueKey = 'value'}) => {
    const choicesByValue = useMemo(() => keyBy(choices, valueKey), [choices, valueKey]);
    return useMemo(() => values.map(value => choicesByValue[value]), [choicesByValue, values]);
};

const MultiSelect = ({choices, values, onChange, valueKey, ...props}) => {
    const items = useMapChoicesToItems({choices, values, valueKey});
    const handleItemSelect = useCallback((item, event) => {
        event.stopPropagation();
        if (values.includes(item[valueKey])) {
            onChange(values.filter(value => item[valueKey] !== value));
        } else {
            onChange([...values, item[valueKey]]);
        }
    }, [onChange, valueKey, values]);
    const handleItemsPaste = useCallback(
        items => onChange([...values, ...items.map(item => item[valueKey])]),
        [onChange, valueKey, values],
    );
    const handleRemove = useCallback(
        item => onChange(values.filter(value => item[valueKey] !== value)),
        [onChange, valueKey, values],
    );

    const itemRenderer = useCallback(
        (item, itemProps) => (
            <Item
                key={item[valueKey]}
                item={item}
                selected={values.includes(item[valueKey])}
                {...itemProps}
            />
        ),
        [valueKey, values],
    );

    return (
        <BPMultiSelect
            tagRenderer={TagRenderer}
            items={choices}
            selectedItems={items}
            onItemSelect={handleItemSelect}
            onItemsPaste={handleItemsPaste}
            onRemove={handleRemove}
            itemRenderer={itemRenderer}
            tagInputProps={tagInputProps}
            itemPredicate={(query, item) => !query || item.label.toLowerCase().includes(query.toLowerCase())}
            {...props}
        />
    );
};

MultiSelect.defaultProps = {
    valueKey: 'value',
};

const ControlledMultiSelect = ({name, control, required, defaultValue, choices, ...props}) => {
    const {field: {value, onChange}} = useController({
        name,
        control,
        rules: {required},
        defaultValue: [],
    });

    return (
        <MultiSelect choices={choices} values={value} onChange={onChange} {...props} />
    );
};

const MultiSelectField = props => (
    <Field {...props}>
        <ControlledMultiSelect />
    </Field>
);

export default MultiSelectField;
