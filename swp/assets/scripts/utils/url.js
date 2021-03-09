const clean = segment => {
    let cleaned = String(segment);

    if (cleaned.startsWith('/')) cleaned = cleaned.substring(1, cleaned.length - 1);
    if (cleaned.endsWith('/')) cleaned = cleaned.substring(0, cleaned.length - 1);

    return cleaned;
};

export const buildURL = (...args) => ['', ...args.filter(Boolean).map(clean), ''].join('/');

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
