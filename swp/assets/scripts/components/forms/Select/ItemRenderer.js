import {MenuItem} from '@blueprintjs/core';

const ItemRenderer = (item, {handleClick, modifiers: {active, disabled}}) => (
    <MenuItem
        key={item.value}
        text={item.label}
        icon={item.icon}
        onClick={handleClick}
        active={active}
        disabled={disabled}
    />
);

export default ItemRenderer;
