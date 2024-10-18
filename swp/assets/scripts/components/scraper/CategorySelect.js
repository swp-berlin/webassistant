import {TagInput as BPTagInput} from '@blueprintjs/core';

import {MultiSelect} from 'components/forms';
import Query from 'components/Query';
import Field from 'components/forms/Field';
import {useController} from 'react-hook-form';

const QueryKey = ['category', 'choices'];

const DisabledCategorySelect = ({name, control, choices, ...props}) => {
    const {field} = useController({name, control});
    const isSelected = field.value.includes;
    const values = choices.filter(({value}) => isSelected(value)).map(({label}) => label);

    return (
        <Field {...props} name={name} disabled>
            <BPTagInput {...props} values={values} />
        </Field>
    );
};

const CategorySelect = ({disabled, ...props}) => {
    const Child = disabled ? DisabledCategorySelect : MultiSelect;

    return (
        <Query queryKey={QueryKey}>
            {choices => <Child {...props} choices={choices} />}
        </Query>
    );
};

export default CategorySelect;
