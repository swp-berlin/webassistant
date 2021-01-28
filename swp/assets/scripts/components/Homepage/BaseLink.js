import classNames from 'classnames';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {Link} from 'react-router-dom';


const BaseLink = ({to, text, icon, className, ...props}) => (
    <Link className={classNames('text-center', 'p-10', 'hover:bg-gray-100', className)} to={to} title={text} {...props}>
        <FontAwesomeIcon icon={icon} size="6x" />
        <span className="block mt-2">
            {text}
        </span>
    </Link>
);

export default BaseLink;
