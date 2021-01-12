import _ from 'utils/i18n';
import {TextInput} from 'components/forms';

import ResolverListForm from '../ResolverListForm';


const SelectorLabel = _('Selector');

const LinkResolverForm = ({form, prefix, level, field}) => {
    const {register, errors} = form;

    return (
        <ResolverListForm form={form} prefix={prefix} level={level}>
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
