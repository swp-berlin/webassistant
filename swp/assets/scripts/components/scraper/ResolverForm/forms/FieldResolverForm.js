import {useController} from 'react-hook-form';
import {Select} from 'components/forms';
import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';

import DataResolverForm from './DataResolverForm';
import AttributeResolverForm from './AttributeResolverForm';
import StaticResolverForm from './StaticResolverForm';


const FieldLabel = _('Field');
const TypeLabel = _('Type');
const ResolverTypeChoices = getChoices('ResolverType');

const FieldTypeChoices = ResolverTypeChoices.filter(choice => ['Data', 'Attribute', 'Static'].includes(choice.value));

const FieldForms = {
    Data: DataResolverForm,
    Attribute: AttributeResolverForm,
    Static: StaticResolverForm,
};

const FieldResolverForm = props => {
    const {form: {control, register, errors}, prefix, field, label, multiple, readOnly} = props;
    const name = `${prefix}.type`;
    const {field: {value, onChange}} = useController({control, name, defaultValue: field.type || 'Data'});

    const Form = FieldForms[value];

    return (
        <div>
            <h2 className="text-lg mb-4">{label}</h2>
            <Select
                name={name}
                label={TypeLabel}
                choices={FieldTypeChoices}
                value={value}
                onChange={onChange}
                disabled={readOnly}
                errors={errors}
            />
            {multiple && <input name="multiple" type="hidden" value={multiple} ref={register} />}
            <Form {...props} />
        </div>
    );
};

FieldResolverForm.defaultProps = {
    label: FieldLabel,
    multiple: false,
    keyed: true,
};

export default FieldResolverForm;
