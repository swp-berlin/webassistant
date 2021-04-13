import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';
import Select from 'components/forms/Select/Select';
import {TagInput} from 'components/forms';
import {useCallback} from 'react';

const FieldLabel = _('Filter on Field');
const ComparatorLabel = _('Comparator');
const ValuesLabel = _('Values');
const RemoveFilterTitle = _('Remove Filter');

const FieldChoices = getChoices('DataResolverKey');
const ComparatorChoices = getChoices('Comparator');


const PublicationFilterForm = ({form: {register, control, errors}, index, data, onRemove}) => {
    const prefix = `filters[${index}]`;
    const handleRemove = useCallback(() => onRemove(index), [index, onRemove]);

    return (
        <>
            <input name={`${prefix}.id`} ref={register({valueAsNumber: true})} type="hidden" defaultValue={data.id} />
            <Select
                className="col-span-4"
                control={control}
                name={`${prefix}.field`}
                label={FieldLabel}
                choices={FieldChoices}
                errors={errors}
                defaultValue={data.field}
                required
            />
            <Select
                className="col-span-3"
                control={control}
                name={`${prefix}.comparator`}
                label={ComparatorLabel}
                choices={ComparatorChoices}
                errors={errors}
                defaultValue={data.comparator}
                required
            />
            <TagInput
                className="col-span-4"
                control={control}
                name={`${prefix}.values`}
                label={ValuesLabel}
                errors={errors}
                defaultValue={data.values}
                required
            />
            <Button
                className="mt-2 col-span-1"
                minimal
                icon="cross"
                onClick={handleRemove}
                title={RemoveFilterTitle}
            />
        </>
    );
};

export default PublicationFilterForm;
