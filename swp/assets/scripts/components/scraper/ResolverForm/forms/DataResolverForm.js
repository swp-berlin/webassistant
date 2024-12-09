import SelectorField from './SelectorField';

const DataResolverForm = props => {
    const {form, prefix, field, children, readOnly} = props;
    const {register, errors} = form;

    return (
        <>
            <SelectorField
                register={register}
                name={`${prefix}.selector`}
                errors={errors}
                defaultValue={field.selector}
                readOnly={readOnly}
                required
            />
            {children}
        </>
    );
};

export default DataResolverForm;
