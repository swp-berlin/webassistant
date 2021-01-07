import {Card, Elevation} from '@blueprintjs/core';

import {useResolverForm} from './ResolverFormContext';


const ResolverForm = ({form, prefix, level, type: defaultType}) => {
    const {watch, register} = form;
    const name = `${prefix}.type`;
    const type = watch(name, defaultType);
    const Form = useResolverForm(type);

    return (
        <Card elevation={Elevation.ONE}>
            <input name={name} ref={register({required: true})} type="hidden" defaultValue={type} />
            {Form && <Form form={form} prefix={prefix} level={level} />}
        </Card>
    );
};

ResolverForm.defaultProps = {
    prefix: '',
    level: 0,
};

export default ResolverForm;
