import {Controller} from 'react-hook-form';
import {Checkbox as BPCheckbox} from '@blueprintjs/core';

const Checkbox = ({control, name, ...props}) => (
    <Controller
        name={name}
        control={control}
        render={({value, onChange, ...controllerProps}) => (
            <BPCheckbox checked={value} onChange={e => onChange(e.target.checked)} {...controllerProps} {...props} />
        )}
    />
);

export default Checkbox;
