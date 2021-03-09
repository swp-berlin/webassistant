import {NonIdealState} from '@blueprintjs/core';
import _ from 'utils/i18n';


const Label = _('No permission');
const Description = _('Your accounts does not have sufficient privileges.');

const NoPermission = props => (
    <NonIdealState icon="disable" title={Label} description={Description} {...props} />
);

export default NoPermission;
