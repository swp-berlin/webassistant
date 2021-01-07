import {useCallback} from 'react';
import {useFieldArray} from 'react-hook-form';

import AddResolverWidget from './AddResolverWidget';
import ResolverForm from './ResolverForm';


const ResolverListForm = ({form, prefix, level, children}) => {
    const {control} = form;
    const name = `${prefix}.resolvers`;
    const {fields, append} = useFieldArray({control, name});

    const handleAdd = useCallback(type => append({type}), [append]);

    return (
        <div>
            {children}

            <div style={{marginLeft: `${(level + 1) * 20}px`}}>
                <AddResolverWidget onAdd={handleAdd} />

                <ul>
                    {(fields.map((field, index) => (
                        <ResolverForm key={field.id} form={form} prefix={`${name}[${index}]`} type={field.type} />
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
