import {useState} from 'react';


export const useControllableState = ({value, defaultValue, onChange}) => {
    const controlled = useState(defaultValue || value);

    if (value !== undefined) return [value, onChange];

    return controlled;
};
