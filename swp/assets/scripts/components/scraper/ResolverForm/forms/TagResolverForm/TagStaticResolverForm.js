import _ from 'utils/i18n';
import {TextInput} from 'components/forms';


const ValueLabel = _('Value');

const TagStaticResolverForm = ({form, prefix, field, children, readOnly}) => {
    const {register, errors} = form;

    return (
        <div>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="TagStatic" />
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

export default TagStaticResolverForm;
