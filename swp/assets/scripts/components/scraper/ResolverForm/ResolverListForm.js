import {useCallback} from 'react';
import {useFieldArray} from 'react-hook-form';

import {getChoices} from 'utils/choices';

import AddResolverWidget from './AddResolverWidget';
import ResolverForm from './ResolverForm';

const ListResolverTypeChoices = getChoices('ListResolverType');

const ResolverListForm = ({form, prefix, level, choices = ListResolverTypeChoices, children}) => {
    const {control} = form;
    const name = `${prefix}.resolvers`;
    const {append, fields, remove} = useFieldArray({control, name});

    const handleAdd = useCallback(type => append({type}), [append]);
    const handleDelete = useCallback(index => remove(index), [remove]);

    return (
        <div>
            {children}
            <div style={{marginLeft: `${(level + 1) * 2}rem`}}>
                <ul className="flex flex-col space-y-4">
                    {(fields.map((field, index) => (
                        <ResolverForm
                            key={field.id}
                            form={form}
                            prefix={`${name}[${index}]`}
                            field={field}
                            onDelete={() => handleDelete(index)}
                        />
                    )))}
                </ul>
                <AddResolverWidget choices={choices} onAdd={handleAdd} />
            </div>
        </div>
    );
};

ResolverForm.defaultProps = {
    level: 0,
};

export default ResolverListForm;
