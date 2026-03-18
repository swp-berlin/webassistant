export const preventDefault = event => event.preventDefault();
export const stopPropagation = event => event.stopPropagation();
export const preventPropagation = event => {
    preventDefault(event);
    stopPropagation(event);
};
