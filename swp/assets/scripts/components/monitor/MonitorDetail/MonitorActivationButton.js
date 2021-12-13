import _ from 'utils/i18n';
import {ActivationButton} from 'components/buttons';


const ActivatedMessage = _('Monitor has been activated');
const DeactivatedMessage = _('Monitor has been deactivated');

const MonitorActivationButton = props => (
    <ActivationButton
        {...props}
        activatedMessage={ActivatedMessage}
        deactivatedMessage={DeactivatedMessage}
    />
);

export default MonitorActivationButton;
