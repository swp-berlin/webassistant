import {useCallback, useState} from 'react';
import {Button} from '@blueprintjs/core';

import {Select} from 'components/forms';


const AddResolverWidget = ({choices, onAdd}) => {
    const [selected, setSelected] = useState(choices[0].value);
    const handleAdd = useCallback(() => onAdd(selected), [selected, onAdd]);

    return (
        <div className="flex space-x-2 mt-8">
            <Select
                className="flex-grow"
                choices={choices}
                value={selected}
                onChange={item => setSelected(item)}
            />
            <div><Button onClick={handleAdd} text="Add" minimal /></div>
        </div>
    );
};

export default AddResolverWidget;
