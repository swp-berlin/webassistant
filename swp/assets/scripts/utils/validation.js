export const isEmail = value => {
    const input = document.createElement('input');

    input.type = 'email';
    input.required = true;
    input.value = value;

    return input.reportValidity();
};
