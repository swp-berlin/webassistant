import {faSearch} from '@fortawesome/free-solid-svg-icons/faSearch';

import _ from 'utils/i18n';
import BaseLink from './BaseLink';


const Label = _('Search');

const SearchLink = ({...props}) => (
    <BaseLink to="/search/" text={Label} icon={faSearch} {...props} />
);

export default SearchLink;
