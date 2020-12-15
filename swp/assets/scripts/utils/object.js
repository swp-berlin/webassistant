export const isString = value => typeof value === 'string';

export const isArray = value => Array.isArray(value);

export const isUndefined = value => typeof value === 'undefined';

export const isNullOrUndefined = value => value === null || isUndefined(value);

export const isFunction = value => typeof value === 'function';

export const get = (obj, path, defaultValue) => {
    const result = path
        .split(/[,[\].]+?/)
        .filter(Boolean)
        .reduce(
            (result, key) => (isNullOrUndefined(result) ? result : result[key]),
            obj,
        );
    return isUndefined(result) || result === obj
        ? obj[path] || defaultValue
        : result;
};
