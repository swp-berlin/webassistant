import {isString, isArray, isObject} from 'utils/object';

const isErrorMessageArray = values => isArray(values) && values.every(value => isString(value));

export const setErrors = (setError, errors, path = '') => {
    if (isErrorMessageArray(errors)) {
        const types = {};

        errors.forEach((msg, idx) => {
            types[`backend-${idx}`] = msg;
        });

        return setError(path, {types});
    }

    if (isArray(errors)) {
        return errors.forEach((error, idx) => setErrors(setError, error, `${path}[${idx}]`));
    }

    if (isObject(errors)) {
        return Object.keys(errors).forEach(key => setErrors(setError, errors[key], path ? `${path}.${key}` : key));
    }
};
