import _ from 'utils/i18n';
import {TextInput} from 'components/forms';


const ValueLabel = _('Value');

const StaticResolverForm = ({form, prefix, field, children, readOnly}) => {
    const {register, errors} = form;

    return (
        <div>
            <TextInput
                register={register({required: true})}
                name={`${prefix}.value`}
                label={ValueLabel}
                errors={errors}
                defaultValue={field.value}
                readOnly={readOnly}
            />
            {children}
        </div>
    );
};

export default StaticResolverForm;
