import _, {interpolate, ngettext} from 'utils/i18n';

import {getPublicationsLabel} from 'components/publication/helper';

const NoPublicationsFound = _('No publications found');

const getRelevanceLabel = count => interpolate(
    ngettext('%s Publication by relevance', '%s Publications by relevance', count), [count], false,
);

const getLabel = (query, count) => (
    query.startsWith('<') && query.includes('>')
        ? getRelevanceLabel(count)
        : getPublicationsLabel(count)
);

const SearchResultHeader = ({query, count, children}) => (
    <header className="flex space-x-4 mb-2">
        <h3>{count ? getLabel(query, count) : NoPublicationsFound}</h3>
        {children}
    </header>
);

export default SearchResultHeader;
