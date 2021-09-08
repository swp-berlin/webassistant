export const isEmail = value => {
    const input = document.createElement('input');

    input.type = 'email';
    input.required = true;
    input.value = value;

    return input.reportValidity();
};

const ZoteroKeyRegex = /[a-zA-Z0-9]+\/(users|groups)\/\d+(\/collections\/[A-Z0-9]+)?\/items\/?/;

export const isZoteroKey = value => ZoteroKeyRegex.test(value);
