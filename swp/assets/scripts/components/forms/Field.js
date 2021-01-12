import {cloneElement} from 'react';
import {FormGroup} from '@blueprintjs/core';
import cN from 'classnames';

import _ from 'utils/i18n';
import {get} from 'utils/object';

import Errors from 'components/forms/Errors';


const RequiredLabel = _('(required)');


const Field = ({children, id, name, label, labelInfo, errors, hasError, className, ...props}) => {
    const fieldErrors = errors && get(errors, name);
    const intent = (hasError || fieldErrors) ? 'danger' : 'none';
    const {required} = props;

    return (
        <FormGroup
            className={cN(className, 'block text-sm font-medium text-gray-700')}
            label={label}
            labelFor={id || name}
            labelInfo={labelInfo || (required && RequiredLabel)}
            intent={intent}
            helperText={fieldErrors && <Errors errors={fieldErrors} />}
        >
            {cloneElement(children, {intent, id: id || name, name, ...props})}
        </FormGroup>
    );
};

export default Field;
