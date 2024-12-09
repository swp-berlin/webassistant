import {useController} from 'react-hook-form';

import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';

import {Select} from 'components/forms';

import BaseResolverForm from './BaseResolverForm';
import DataResolverForm from './DataResolverForm';
import AttributeResolverForm from './AttributeResolverForm';
import StaticResolverForm from './StaticResolverForm';

const FieldLabel = _('Field');
const TypeLabel = _('Type');
const ResolverTypeChoices = getChoices('ResolverType');

const FieldTypeChoices = ResolverTypeChoices.filter(choice => ['Data', 'Attribute', 'Static'].includes(choice.value));

const ResolverLabels = Object.fromEntries(ResolverTypeChoices.map(choice => [choice.value, choice.label]));

const FieldForms = {
    Data: DataResolverForm,
    Attribute: AttributeResolverForm,
    Static: StaticResolverForm,
};

const getLabel = type => ResolverLabels[type] || FieldLabel;

const FieldResolverForm = props => {
    const {form: {control, register, errors}, prefix, field, readOnly} = props;
    const {field: {value, onChange}} = useController({
        control,
        name: `${prefix}.resolver.type`,
        defaultValue: field?.resolver?.type || 'Data',
    });

    const Form = FieldForms[value];
    const label = getLabel(field?.type);

    return (
        <BaseResolverForm label={label}>
            <input name={`${prefix}.type`} type="hidden" value={field?.type} ref={register()} />
            <Select
                name={`${prefix}.resolver.type`}
                label={TypeLabel}
                choices={FieldTypeChoices}
                value={value}
                onChange={onChange}
                disabled={readOnly}
                errors={errors}
            />
            <Form {...props} prefix={`${prefix}.resolver`} field={field?.resolver || {}} />
        </BaseResolverForm>
    );
};

export default FieldResolverForm;
