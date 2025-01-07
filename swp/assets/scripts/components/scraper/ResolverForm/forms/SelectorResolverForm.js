import BaseResolverForm from './BaseResolverForm';
import DataResolverForm from './DataResolverForm';

const SelectorResolverForm = ({label, type, prefix, form, ...props}) => {
    const ref = form.register({required: true});

    return (
        <BaseResolverForm label={label}>
            <input type="hidden" name={`${prefix}.type`} defaultValue={type} ref={ref} />
            <DataResolverForm prefix={prefix} form={form} {...props} />
        </BaseResolverForm>
    );
};

export default SelectorResolverForm;
