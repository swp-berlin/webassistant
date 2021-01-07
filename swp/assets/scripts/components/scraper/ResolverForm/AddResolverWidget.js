import {useCallback, useState} from 'react';
import {Button} from '@blueprintjs/core';

import {Select} from 'components/forms';

// FIXME
const ResolverChoices = [{label: 'List', value: 'List'}];

const AddResolverWidget = ({onAdd}) => {
    const [selected, setSelected] = useState(ResolverChoices[0].value);
    const handleAdd = useCallback(() => onAdd(selected), [selected, onAdd]);

    return (
        <div className="flex">
            <Select
                className="flex-grow"
                choices={ResolverChoices}
                value={selected}
                onChange={item => setSelected(item)}
            />
            <div><Button onClick={handleAdd} text="Add" minimal /></div>
        </div>
    );
};

export default AddResolverWidget;
