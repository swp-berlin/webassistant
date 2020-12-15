export const setErrors = (setError, errors) => {
    Object.keys(errors).forEach(name => {
        const fieldErrors = {};

        errors[name].forEach((message, index) => {
            fieldErrors[`backend-${index}`] = message;
        });

        setError(name, fieldErrors);
    });
};
