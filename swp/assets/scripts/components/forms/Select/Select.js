import {Button} from '@blueprintjs/core';
import {Select as BPSelect} from '@blueprintjs/select';

import Field from '../Field';
import SelectController from './SelectController';

const EMPTY = '---';

const Select = ({value, ...props}) => (
    <BPSelect {...props} filterable={false}>
        <Button
            text={(value && value.label) || EMPTY}
            alignText="left"
            rightIcon="caret-down"
            fill
        />
    </BPSelect>
);

const SelectField = ({name, ...props}) => (
    <Field name={name} {...props}>
        <SelectController name={name} as={Select} />
    </Field>
);

export default SelectField;
