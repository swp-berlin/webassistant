import {Intent, Position, Toaster} from '@blueprintjs/core';

const toaster = Toaster.create({
    className: 'toaster',
    position: Position.TOP,
});

export const showToast = (message, intent = Intent.SUCCESS, options = {}) => toaster.show({
    ...options,
    message,
    intent,
});

export default toaster;
