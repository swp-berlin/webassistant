import _ from 'utils/i18n';
import {TextInput} from 'components/forms';
import {getChoices} from 'utils/choices';
import {Select} from 'components/forms/Select';


const KeyLabel = _('Field');
const ValueLabel = _('Value');

const KeyChoices = getChoices('DataResolverKey');

const StaticResolverForm = ({form, prefix, field, children}) => {
    const {register, errors} = form;

    return (
        <div>
            <Select
                control={form.control}
                name={`${prefix}.key`}
                label={KeyLabel}
                choices={KeyChoices}
                errors={errors}
                defaultValue={field.key || KeyChoices[0].value}
            />
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

export default StaticResolverForm;
