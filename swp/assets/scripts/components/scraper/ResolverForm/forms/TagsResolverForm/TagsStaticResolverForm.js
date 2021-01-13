import _ from 'utils/i18n';
import {TextInput} from 'components/forms';


const ValueLabel = _('Value');

const TagsStaticResolverForm = ({form, prefix, field, children}) => {
    const {register, errors} = form;

    return (
        <div>
            <TextInput
                register={register({required: true})}
                name={`${prefix}.value`}
                label={ValueLabel}
                errors={errors}
                defaultValue={field.value}
            />
            {children}
        </div>
    );
};

export default TagsStaticResolverForm;
