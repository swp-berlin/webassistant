import _ from 'utils/i18n';

import SelectorField from '../SelectorField';


const DataLabel = _('Data');
const SelectorLabel = _('Selector');

const TagDataResolverForm = ({form, prefix, field, readOnly}) => {
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
                required
                readOnly={readOnly}
            />
        </div>
    );
};

export default TagDataResolverForm;
