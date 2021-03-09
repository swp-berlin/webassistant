import {InputGroup} from '@blueprintjs/core';

import Field from './Field';

const TextInput = ({register, inputRef, ...props}) => (
    <Field {...props}>
        <InputGroup inputRef={register || inputRef} />
    </Field>
);

export default TextInput;
