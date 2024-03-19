import {Children, cloneElement, useMemo, useRef} from 'react';

export const useRegister = (register, errors) => {
    const registerRef = useRef(null);

    registerRef.current = {register, errors};

    return useMemo(
        () => function Register({required = false, children}) {
            const child = Children.only(children);
            const {register, errors} = registerRef.current;

            return cloneElement(child, {register: register({required}), errors, required});
        },
        [registerRef],
    );
};
