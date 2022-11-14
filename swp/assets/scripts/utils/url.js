import trim from 'lodash/trim';

export const Slash = '/';

export const clean = url => trim(url, Slash);

export const buildURL = (...args) => ['', ...args.map(clean).filter(Boolean), ''].join(Slash);

export const withParams = (url, params) => {
    const urlSearchParams = new URLSearchParams();

    Object.keys(params).forEach(key => {
        const value = params[key];

        if (value instanceof Array) {
            value.forEach(value => urlSearchParams.append(key, value));
        } else {
            urlSearchParams.append(key, value);
        }
    });

    return `${url}?${urlSearchParams.toString()}`;
};
