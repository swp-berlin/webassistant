import {NumericInput as BPNumericInput} from '@blueprintjs/core';

import Field from './Field';

const NumericInput = ({register, inputRef, ...props}) => (
    <Field {...props}>
        <BPNumericInput inputRef={register || inputRef} />
    </Field>
);

export default NumericInput;
