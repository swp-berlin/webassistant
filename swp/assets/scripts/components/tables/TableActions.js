import {ButtonGroup} from '@blueprintjs/core';
import classNames from 'classnames';


const TableActions = ({children, className, ...props}) => (
    <ButtonGroup className={classNames('table-actions', 'flex', 'justify-end', 'mt-5', className)} {...props}>
        {children}
    </ButtonGroup>
);

export default TableActions;
