import {NonIdealState} from '@blueprintjs/core';

import _ from 'utils/i18n';


const Label = _('No items');

const EmptyRow = ({colSpan, title}) => (
    <tr>
        <td colSpan={colSpan}>
            <NonIdealState title={title || Label} />
        </td>
    </tr>
);

export default EmptyRow;
