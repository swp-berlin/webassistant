import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';
import classNames from 'classnames';


const BaseLink = ({to, icon, children}) => (
    <Link to={to} className={classNames('bp3-button', 'bp3-minimal', icon && `bp3-icon-${icon}`)}>
        {children}
    </Link>
);

BaseLink.propTypes = {
    ...Link.propTypes,
    icon: PropTypes.string,
};

BaseLink.defaultProps = {
    icon: null,
};

export default BaseLink;
