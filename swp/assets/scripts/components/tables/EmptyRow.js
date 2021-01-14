import PropTypes from 'prop-types';
import {NonIdealState} from '@blueprintjs/core';

import _ from 'utils/i18n';


const Label = _('No items');

const EmptyRow = ({colSpan, title}) => (
    <tr>
        <td colSpan={colSpan}>
            <NonIdealState title={title} />
        </td>
    </tr>
);

EmptyRow.defaultProps = {
    title: Label,
};

EmptyRow.propTypes = {
    colSpan: PropTypes.number.isRequired,
    title: PropTypes.string,
};

export default EmptyRow;
