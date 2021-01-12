import {NumericInput as BPNumericInput} from '@blueprintjs/core';
import {Controller} from 'react-hook-form';

import Field from './Field';


const NumericInput = ({control, inputRef, name, ...props}) => (
    <Field name={name} {...props}>
        <Controller
            control={control}
            name={name}
            render={({onChange, ref, ...controlProps}) => (
                <BPNumericInput
                    {...props}
                    {...controlProps}
                    onValueChange={valueAsNumber => onChange(valueAsNumber)}
                    minorStepSize={null}
                    allowNumericCharactersOnly
                />
            )}
        />
    </Field>
);

export default NumericInput;
