import {Link, useLocation} from 'react-router-dom';
import classNames from 'classnames';

import _ from 'utils/i18n';


const Label = _('Back');

export const useBackURL = to => {
    const {state} = useLocation();
    return (state && state.referrer) || to;
};

const BackButton = ({to, label, icon, ...props}) => (
    <Link className={classNames('bp3-button', icon && `bp3-icon-${icon}`)} to={useBackURL(to)} {...props}>
        {label}
    </Link>
);

BackButton.defaultProps = {
    to: '..',
    label: Label,
    icon: 'chevron-left',
};

export default BackButton;
