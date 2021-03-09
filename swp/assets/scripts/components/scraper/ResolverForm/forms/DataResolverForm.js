import _ from 'utils/i18n';

import SelectorField from './SelectorField';


const SelectorLabel = _('Selector');

const DataResolverForm = props => {
    const {form, prefix, field, children, readOnly} = props;
    const {register, errors} = form;

    return (
        <>
            <SelectorField
                register={register}
                name={`${prefix}.selector`}
                label={SelectorLabel}
                errors={errors}
                defaultValue={field.selector}
                required
                readOnly={readOnly}
            />
            {children}
        </>
    );
};

export default DataResolverForm;
