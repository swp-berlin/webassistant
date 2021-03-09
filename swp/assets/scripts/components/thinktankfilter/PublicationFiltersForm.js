import {useCallback} from 'react';
import {useFieldArray} from 'react-hook-form';
import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';

import PublicationFilterForm from './PublicationFilterForm';


const AddFilterLabel = _('Add Filter');

const EmptyThinktankFilter = {
    field: null,
    comparator: null,
    value: '',
};

const PublicationFiltersForm = ({form}) => {
    const {fields: publicationFilers, append, remove} = useFieldArray({
        control: form.control,
        name: 'filters',
        keyName: 'fieldID',
    });

    const handleAdd = useCallback(() => append(EmptyThinktankFilter), [append]);
    const handleRemove = useCallback(index => remove(index), [remove]);

    return (
        <div className="my-8">
            <h4 className="mb-4">Filters</h4>
            {publicationFilers.map((filter, index) => (
                <PublicationFilterForm
                    key={filter.fieldID}
                    form={form}
                    index={index}
                    data={filter}
                    onRemove={handleRemove}
                />
            ))}
            <Button minimal onClick={handleAdd} icon="plus" text={AddFilterLabel} />
        </div>
    );
};

export default PublicationFiltersForm;
