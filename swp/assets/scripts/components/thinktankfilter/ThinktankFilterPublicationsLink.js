import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';

import {getThinktankFilterPublicationsURL} from './helper';


const ThinktankFilterPublicationsLink = ({id, monitorID, count, onlyNew, children, ...props}) => (
    <Link to={getThinktankFilterPublicationsURL(id, monitorID, onlyNew)} {...props}>
        {children || count}
    </Link>
);

ThinktankFilterPublicationsLink.defaultProps = {
    count: 0,
    onlyNew: false,
    children: null,
};

ThinktankFilterPublicationsLink.propTypes = {
    id: PropTypes.number.isRequired,
    monitorID: PropTypes.number.isRequired,
    count: PropTypes.number,
    onlyNew: PropTypes.bool,
    children: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.node),
        PropTypes.node,
    ]),
};

export default ThinktankFilterPublicationsLink;
