import {useCallback} from 'react';
import {useFieldArray} from 'react-hook-form';

import AddResolverWidget from './AddResolverWidget';
import ResolverForm from './ResolverForm';


const ResolverListForm = ({form, prefix, level, children}) => {
    const {control} = form;
    const name = `${prefix}.resolvers`;
    const {fields, prepend, remove} = useFieldArray({control, name});

    const handleAdd = useCallback(type => prepend({type}), [prepend]);
    const handleDelete = useCallback(index => remove(index), [remove]);

    return (
        <div>
            {children}
            <div style={{marginLeft: `${(level + 1) * 2}rem`}}>
                <AddResolverWidget onAdd={handleAdd} />

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
            </div>
        </div>
    );
};

ResolverForm.defaultProps = {
    level: 0,
};

export default ResolverListForm;
