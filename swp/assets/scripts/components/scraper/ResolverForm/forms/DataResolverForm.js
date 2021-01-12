import _ from 'utils/i18n';
import {TextInput} from 'components/forms';
import {getChoices} from 'utils/choices';
import {Select} from 'components/forms/Select';


const KeyLabel = _('Field');
const SelectorLabel = _('Selector');

const KeyChoices = getChoices('DataResolverKey');

const DataResolverForm = ({form, prefix, field, children}) => {
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
                name={`${prefix}.selector`}
                label={SelectorLabel}
                errors={errors}
                defaultValue={field.selector}
            />
            {children}
        </div>
    );
};

export default DataResolverForm;
