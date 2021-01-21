import _ from 'utils/i18n';
import {TextInput} from 'components/forms';

import ResolverListForm from '../ResolverListForm';


const LinkLabel = _('Link');
const SelectorLabel = _('Selector');

const LinkResolverForm = ({form, prefix, level, field}) => {
    const {register, errors} = form;

    return (
        <ResolverListForm form={form} prefix={prefix} level={level}>
            <h2 className="text-lg mb-4">{LinkLabel}</h2>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="Link" />
            <TextInput
                register={register({required: true})}
                name={`${prefix}.selector`}
                label={SelectorLabel}
                errors={errors}
                defaultValue={field.selector}
            />
        </ResolverListForm>
    );
};

export default LinkResolverForm;
