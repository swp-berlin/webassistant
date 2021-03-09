import {faBriefcase} from '@fortawesome/free-solid-svg-icons/faBriefcase';

import _ from 'utils/i18n';
import BaseLink from './BaseLink';


const Label = _('Monitoring Profiles');

const MonitorLink = ({...props}) => (
    <BaseLink to="/monitor/" text={Label} icon={faBriefcase} {...props} />
);

export default MonitorLink;
