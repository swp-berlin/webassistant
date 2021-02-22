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
    const {form: {control, errors}, prefix, field, readOnly} = props;
    const name = `${prefix}.type`;
    const {field: {value, onChange}} = useController({control, name, defaultValue: field.type || 'Data'});

    const Form = FieldForms[value];

    return (
        <div>
            <h2 className="text-lg mb-4">{FieldLabel}</h2>
            <Select
                name={name}
                label={TypeLabel}
                choices={FieldTypeChoices}
                value={value}
                onChange={onChange}
                disabled={readOnly}
                errors={errors}
            />
            {Form && <Form {...props} />}
        </div>
    );
};

export default FieldResolverForm;
