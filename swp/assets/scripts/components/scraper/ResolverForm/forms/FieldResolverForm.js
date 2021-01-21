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
    const {form: {control, watch}, prefix, field} = props;

    const type = watch(`${prefix}.type`);
    const Form = FieldForms[type];

    return (
        <div>
            <h2 className="text-lg mb-4">{FieldLabel}</h2>
            <Select
                control={control}
                name={`${prefix}.type`}
                label={TypeLabel}
                choices={FieldTypeChoices}
                defaultValue={field.type || 'Data'}
            />
            <Form {...props} />
        </div>
    );
};

export default FieldResolverForm;
