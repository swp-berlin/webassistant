import {TagInput as BPTagInput} from '@blueprintjs/core';
import {useController} from 'react-hook-form';

import _ from 'utils/i18n';

import Field from './Field';


const validate = (items, required) => {
    if (required && !items.length) {
        return _('At least one item is required');
    }

    return true;
};

const preventSubmitOnEnter = e => e.key === 'Enter' && e.preventDefault();

const ControlledTagInput = ({control, name, required, defaultValue, ...props}) => {
    const {field: {onChange, onBlur, value, ref}} = useController({
        control,
        name,
        defaultValue,
        rules: {validate: {required: items => validate(items, required)}},
    });

    return (
        <BPTagInput
            values={value}
            onChange={onChange}
            inputProps={{onBlur, onKeyPress: preventSubmitOnEnter}}
            inputRef={inputRef => { ref.current = inputRef; }}
            {...props}
        />
    );
};

ControlledTagInput.defaultProps = {
    required: false,
    defaultValues: [],
};

const TagInput = props => (
    <Field {...props}>
        <ControlledTagInput />
    </Field>
);

export default TagInput;
