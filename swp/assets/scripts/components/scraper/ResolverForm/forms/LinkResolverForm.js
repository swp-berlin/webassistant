import _ from 'utils/i18n';

import ResolverListForm from '../ResolverListForm';
import SelectorField from './SelectorField';


const LinkLabel = _('Link');
const SelectorLabel = _('Selector');

const LinkResolverForm = ({form, prefix, level, field, readOnly}) => {
    const {register, errors} = form;

    return (
        <ResolverListForm form={form} prefix={prefix} level={level} readOnly={readOnly}>
            <h2 className="text-lg mb-4">{LinkLabel}</h2>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="Link" />
            <SelectorField
                register={register}
                name={`${prefix}.selector`}
                label={SelectorLabel}
                errors={errors}
                defaultValue={field.selector}
                required
                readOnly={readOnly}
            />
        </ResolverListForm>
    );
};

export default LinkResolverForm;
