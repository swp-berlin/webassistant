import {faWarehouse} from '@fortawesome/free-solid-svg-icons/faWarehouse';

import _ from 'utils/i18n';
import BaseLink from './BaseLink';


const Label = _('Thinktanks & Scrapers');

const ThinktankLink = props => (
    <BaseLink to="/thinktank/" text={Label} icon={faWarehouse} {...props} />
);

export default ThinktankLink;
