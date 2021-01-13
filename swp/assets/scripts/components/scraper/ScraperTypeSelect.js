import {forwardRef, useCallback, useEffect, useRef, useState} from 'react';
import {Controller} from 'react-hook-form';

import ScraperTypes from 'schemes/scraperTypes';
import {Select} from 'components/forms';

import ConfigResetWarning from './ConfigResetWarning';


const ScraperTypeSelect = forwardRef(({form, value, onChange, ...props}, ref) => {
    const mounted = useRef(false);
    const [selected, setSelected] = useState(null);

    const handleItemSelect = useCallback(item => value !== item.value && setSelected(item.value), [value]);


    const handleConfirm = useCallback(() => {
        onChange(selected);
        setSelected(null);
    }, [onChange, selected]);

    const handleAbort = useCallback(() => setSelected(null), []);

    const {getValues, reset} = form;

    useEffect(() => {
        if (mounted.current) {
            const scraperType = ScraperTypes.find(scraperType => scraperType.value === value);
            if (scraperType) reset({...getValues(), data: scraperType.defaults});
        } else {
            mounted.current = true;
        }
    }, [getValues, reset, value]);

    return (
        <>
            <ConfigResetWarning isOpen={!!selected} onConfirm={handleConfirm} onAbort={handleAbort} />
            <Select value={value} inputRef={ref} onItemSelect={handleItemSelect} {...props} />
        </>
    );
});

const ControlledScraperTypeSelect = ({form, name, ...props}) => (
    <Controller
        control={form.control}
        name={name}
        render={controllerProps => (
            <ScraperTypeSelect form={form} {...controllerProps} {...props} />
        )}
    />
);

export default ControlledScraperTypeSelect;
