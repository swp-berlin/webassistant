import _ from 'utils/i18n';

import {TextInput} from 'components/forms';


const DocumentLabel = _('Document');
const SelectorLabel = _('Selector');

const DocumentResolverForm = ({form, prefix, field}) => {
    const {register, errors} = form;

    return (
        <div>
            <h2 className="text-lg mb-4">{DocumentLabel}</h2>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="Document" />
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
