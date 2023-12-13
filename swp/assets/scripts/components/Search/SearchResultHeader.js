import _ from 'utils/i18n';

import {getPublicationsLabel} from 'components/publication/helper';

const NoPublicationsFound = _('No publications found');

const SearchResultHeader = ({count, children}) => (
    <header className="flex space-x-4 mb-2">
        <h3>{count ? getPublicationsLabel(count) : NoPublicationsFound}</h3>
        {children}
    </header>
);

export default SearchResultHeader;
