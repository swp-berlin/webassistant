import _ from 'utils/i18n';

import FieldResolverForm from './FieldResolverForm';


const AuthorsLabel = _('Authors');

const AuthorsResolver = props => {
    const {form: {register, watch}, prefix} = props;
    const field = watch(`${prefix}.resolver`, {type: 'Data'});

    return (
        <>
            <input name={`${prefix}.type`} type="hidden" value="Authors" ref={register} />
            <FieldResolverForm
                {...props}
                prefix={`${prefix}.resolver`}
                label={AuthorsLabel}
                field={field}
                fieldKey="authors"
            />
        </>
    );
};

export default AuthorsResolver;
