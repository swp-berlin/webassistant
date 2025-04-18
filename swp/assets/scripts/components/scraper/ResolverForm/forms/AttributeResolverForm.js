import _ from 'utils/i18n';

import {TextInput} from 'components/forms';

import DataResolverForm from './DataResolverForm';

const AttributeLabel = _('Attribute');

const AttributeResolverForm = props => {
    const {form: {register, errors}, prefix, field, readOnly} = props;

    return (
        <DataResolverForm {...props}>
            <TextInput
                register={register({required: true})}
                name={`${prefix}.attribute`}
                label={AttributeLabel}
                errors={errors}
                defaultValue={field.attribute}
                readOnly={readOnly}
            />
        </DataResolverForm>
    );
};

export default AttributeResolverForm;
