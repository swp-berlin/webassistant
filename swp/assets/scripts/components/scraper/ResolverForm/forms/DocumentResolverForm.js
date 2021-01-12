import _ from 'utils/i18n';

import {TextInput} from 'components/forms';

const SelectorLabel = _('Selector');


const DocumentResolverForm = ({form, prefix, field}) => {
    const {register, errors} = form;

    return (
        <div>
            <TextInput
                register={register({required: true})}
                name={`${prefix}.selector`}
                label={SelectorLabel}
                errors={errors}
                defaultValue={field.selector}
            />
        </div>
    );
};

export default DocumentResolverForm;
