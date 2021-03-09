import {TextArea as BPTextArea} from '@blueprintjs/core';

import Field from './Field';

const TextArea = ({register, inputRef, ...props}) => (
    <Field {...props}>
        <BPTextArea inputRef={register || inputRef} />
    </Field>
);

export default TextArea;
