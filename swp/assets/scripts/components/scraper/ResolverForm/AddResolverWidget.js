import {useCallback, useState} from 'react';
import {Button} from '@blueprintjs/core';

import {getChoices} from 'utils/choices';
import {Select} from 'components/forms';


const ResolverTypeChoices = getChoices('ResolverType');

const AddResolverWidget = ({onAdd}) => {
    const [selected, setSelected] = useState(ResolverTypeChoices[0].value);
    const handleAdd = useCallback(() => onAdd(selected), [selected, onAdd]);

    return (
        <div className="flex space-x-2 mt-8">
            <Select
                className="flex-grow"
                choices={ResolverTypeChoices}
                value={selected}
                onChange={item => setSelected(item)}
            />
            <div><Button onClick={handleAdd} text="Add" minimal /></div>
        </div>
    );
};

export default AddResolverWidget;
