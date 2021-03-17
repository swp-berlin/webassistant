import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';


export const getMonitorPublicationsURL = (id, onlyNew = false) => (
    onlyNew ? `/monitor/${id}/publications/new/` : `/monitor/${id}/publications/`
);

const MonitorPublicationsLink = ({id, count, onlyNew, children, ...props}) => (
    <Link to={getMonitorPublicationsURL(id, onlyNew)} {...props}>
        {children || count}
    </Link>
);

MonitorPublicationsLink.defaultProps = {
    count: 0,
    onlyNew: false,
    children: null,
};

MonitorPublicationsLink.propTypes = {
    id: PropTypes.number.isRequired,
    count: PropTypes.number,
    onlyNew: PropTypes.bool,
    children: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.node),
        PropTypes.node,
    ]),
};

export default MonitorPublicationsLink;
