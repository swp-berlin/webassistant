import _ from 'utils/i18n';
import {TextInput} from 'components/forms';
import SelectorField from 'components/scraper/ResolverForm/forms/SelectorField';


const DataLabel = _('Data');
const SelectorLabel = _('Selector');

const TagDataResolverForm = ({form, prefix, field}) => {
    const {register, errors} = form;

    return (
        <div>
            <h2 className="text-lg mb-4">{DataLabel}</h2>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="TagData" />
            <SelectorField
                register={register}
                name={`${prefix}.selector`}
                label={SelectorLabel}
                errors={errors}
                defaultValue={field.selector}
            />
        </div>
    );
};

export default TagDataResolverForm;
