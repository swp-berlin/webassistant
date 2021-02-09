import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';
import Select from 'components/forms/Select/Select';
import {TextInput} from 'components/forms';
import {useCallback} from 'react';

const FieldLabel = _('Filter on Field');
const ComparatorLabel = _('Comparator');
const ValueLabel = _('Value');
const RemoveFilterTitle = _('Remove Filter');

const FieldChoices = getChoices('DataResolverKey');
const ComparatorChoices = getChoices('Comparator');


const PublicationFilterForm = ({form: {register, control, errors}, index, data, onRemove}) => {
    const prefix = `filters[${index}]`;
    const handleRemove = useCallback(() => onRemove(index), [index, onRemove]);

    return (
        <div className="grid grid-cols-4 justify-items-stretch space-x-4 items-center">
            <input name={`${prefix}.id`} ref={register({valueAsNumber: true})} type="hidden" defaultValue={data.id} />
            <Select
                control={control}
                name={`${prefix}.field`}
                label={FieldLabel}
                choices={FieldChoices}
                errors={errors}
                defaultValue={data.field}
                required
            />
            <Select
                control={control}
                name={`${prefix}.comparator`}
                label={ComparatorLabel}
                choices={ComparatorChoices}
                errors={errors}
                defaultValue={data.comparator}
                required
            />
            <TextInput
                register={register({required: true})}
                name={`${prefix}.value`}
                label={ValueLabel}
                errors={errors}
                defaultValue={data.value}
            />
            <Button
                className="mt-2 justify-self-start"
                minimal
                icon="cross"
                onClick={handleRemove}
                title={RemoveFilterTitle}
            />
        </div>
    );
};

export default PublicationFilterForm;
