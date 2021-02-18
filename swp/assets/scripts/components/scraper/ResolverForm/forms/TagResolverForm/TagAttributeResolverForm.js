import _ from 'utils/i18n';

import {TextInput} from 'components/forms';
import SelectorField from 'components/scraper/ResolverForm/forms/SelectorField';


const SelectorLabel = _('Selector');
const AttributeLabel = _('Attribute');

const TagAttributeResolverForm = props => {
    const {form: {register, errors}, prefix, field, readOnly} = props;

    return (
        <div>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="TagAttribute" />
            <SelectorField
                register={register}
                name={`${prefix}.selector`}
                label={SelectorLabel}
                errors={errors}
                defaultValue={field.selector}
                readOnly={readOnly}
            />
            <TextInput
                register={register()}
                name={`${prefix}.attribute`}
                label={AttributeLabel}
                errors={errors}
                defaultValue={field.attribute}
                readOnly={readOnly}
            />
        </div>
    );
};

export default TagAttributeResolverForm;
