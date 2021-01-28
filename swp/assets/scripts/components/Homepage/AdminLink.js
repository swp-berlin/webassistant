import classNames from 'classnames';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faTools} from '@fortawesome/free-solid-svg-icons/faTools';

import _ from 'utils/i18n';


const Label = _('Admin');

const AdminLink = ({className, ...props}) => (
    <a href="/admin/" className={classNames('text-center', 'p-10', 'hover:bg-gray-100', className)} {...props}>
        <FontAwesomeIcon icon={faTools} size="6x" />
        <span className="block mt-2">
            {Label}
        </span>
    </a>
);

export default AdminLink;
