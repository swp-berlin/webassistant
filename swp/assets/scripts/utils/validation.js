export const isEmail = value => {
    const input = document.createElement('input');

    input.type = 'email';
    input.required = true;
    input.value = value;

    return input.reportValidity();
};

export const isZoteroKey = value => (
    /[a-zA-Z0-9]+\/(users|groups)\/\d+(\/w+)*\/?/.test(value)
);
