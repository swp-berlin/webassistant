import {Button, Card, Elevation} from '@blueprintjs/core';

import {useResolverForm} from './ResolverFormContext';


const ResolverForm = ({form, prefix, level, type: defaultType, onDelete}) => {
    const {watch, register} = form;
    const name = `${prefix}.type`;
    const type = watch(name, defaultType);
    const Form = useResolverForm(type);

    return (
        <Card className="relative" elevation={Elevation.ONE}>
            {onDelete && <Button small minimal className="absolute top-2 right-2" icon="trash" onClick={onDelete} />}
            <input name={name} ref={register({required: true})} type="hidden" defaultValue={type} />
            {Form ? <Form form={form} prefix={prefix} level={level} /> : <p>{`resolver Type "${type}" unsupported`}</p>}
        </Card>
    );
};

ResolverForm.defaultProps = {
    prefix: '',
    level: 0,
};

export default ResolverForm;
