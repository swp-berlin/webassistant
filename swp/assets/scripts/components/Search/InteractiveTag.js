import {useCallback} from 'react';
import {Tag} from '@blueprintjs/core';

const InteractiveTag = ({value, label, selected, onClick}) => {
    const handleClick = useCallback(() => onClick(value), [value, onClick]);

    return (
        <Tag onClick={handleClick} interactive>
            {`${selected ? '-' : '+'} ${label}`}
        </Tag>
    );
};

export default InteractiveTag;
