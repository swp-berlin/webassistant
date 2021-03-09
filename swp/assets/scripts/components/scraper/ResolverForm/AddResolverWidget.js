import {useCallback, useState} from 'react';
import {Button} from '@blueprintjs/core';

import {Select} from 'components/forms';
import _ from 'utils/i18n';


const Label = _('Add');

const AddResolverWidget = ({choices, onAdd, readOnly}) => {
    const [selected, setSelected] = useState(choices[0].value);
    const handleAdd = useCallback(() => onAdd(selected), [selected, onAdd]);

    return (
        <div className="flex space-x-2 mt-8">
            <Select
                className="flex-grow"
                choices={choices}
                value={selected}
                onChange={item => setSelected(item)}
                disabled={readOnly}
            />
            <Button disabled={readOnly} className="mb-4" onClick={handleAdd} text={Label} minimal />
        </div>
    );
};

export default AddResolverWidget;
