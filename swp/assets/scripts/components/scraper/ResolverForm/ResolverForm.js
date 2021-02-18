import {Button, Card, Elevation} from '@blueprintjs/core';

import _, {interpolate} from 'utils/i18n';

import {useResolverForm} from './ResolverFormContext';


const UnsupportedTypeLabel = _('Resolver Type %(type)s unsupported');

const ResolverForm = ({form, prefix, level, field = {}, onDelete, readOnly}) => {
    const {watch} = form;
    const name = `${prefix}.type`;
    const type = field.type || watch(name, field.type);
    const Form = useResolverForm(type);

    return (
        <Card className="relative" elevation={Elevation.ONE}>
            {onDelete && (
                <Button
                    small
                    minimal
                    className="absolute top-5 right-5"
                    icon="trash"
                    onClick={onDelete}
                    disabled={readOnly}
                />
            )}
            {Form ? (
                <Form form={form} prefix={prefix} level={level} field={field} readOnly={readOnly} />
            ) : <p>{interpolate(UnsupportedTypeLabel, {type})}</p>}
        </Card>
    );
};

ResolverForm.defaultProps = {
    prefix: '',
    level: 0,
};

export default ResolverForm;
