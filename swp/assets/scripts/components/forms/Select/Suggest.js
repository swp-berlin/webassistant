import {useCallback, useRef} from 'react';
import {Suggest as BPSuggest} from '@blueprintjs/select';
import {Button} from '@blueprintjs/core';

import Field from '../Field';
import SelectController from './SelectController';


const preventSubmit = event => event.key === 'Enter' && event.preventDefault();

const Suggest = ({id, name, choices, intent, value, ...props}) => {
    const inputRef = useRef();
    const handleCaretDownClick = useCallback(() => inputRef.current.focus(), []);

    return (
        <BPSuggest
            inputProps={{
                id,
                name,
                inputRef: ref => { inputRef.current = ref; },
                intent,
                rightElement: <Button minimal rightIcon="caret-down" onClick={handleCaretDownClick} />,
                autoComplete: 'off',
                onKeyPress: preventSubmit,
            }}
            resetOnSelect
            selectedItem={value}
            fill
            resetOnClose
            {...props}
        />
    );
};


const SuggestField = ({name, ...props}) => (
    <Field name={name} {...props}>
        <SelectController name={name} as={Suggest} />
    </Field>
);


export default SuggestField;
