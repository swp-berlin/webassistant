import {useCallback, useState} from 'react';
import {useSearchParams} from 'react-router-dom';

import Page from 'components/Page';
import {useBreadcrumb} from 'components/Navigation';
import {Query} from 'components/Fetch';
import _ from 'utils/i18n';

import SearchForm from './SearchForm';
import SearchResult from './SearchResult';
import parseISO from 'date-fns/parseISO';
import formatISO from 'date-fns/formatISO';

const SearchLabel = _('Search');

const formatDate = date => date && formatISO(date, { representation: 'date' });
const parseDate = date => date ? parseISO(date) : null;
const updateSearchParams = values => prev => {
    Object.keys(values).forEach(name => prev.set(name, values[name]));
    return prev;
};

const SearchPage = () => {
    useBreadcrumb('/search/', SearchLabel);
    const [searchParams, setSearchParams] = useSearchParams();

    const [query, setQuery] = useState(searchParams.get('query') || '');
    const handleQueryChange = useCallback(term => setQuery(term), []);

    const [dates, setDates] = useState(
        () => [parseDate(searchParams.get('start_date')), parseDate(searchParams.get('end_date'))]
    );
    const handleDatesChange = useCallback(dates => setDates(dates), []);

    const [tag, setTag] = useState(searchParams.get('tag'));
    const handleSelectTag = useCallback(tag => {
        setTag(tag);
        setSearchParams(updateSearchParams({tag}));
    }, []);

    const [params, setParams] = useState({query});

    const handleSearch = useCallback(() => {
        const params = {query};
        const [startDate, endDate] = dates;
        if (startDate) params.start_date = formatDate(startDate);
        if (endDate) params.end_date = formatDate(endDate);
        if (tag) params.tag = tag;

        setParams(params);
        setSearchParams(updateSearchParams(params));
    }, [query, dates, tag]);

    return (
        <Page title={SearchLabel}>
            <SearchForm
                query={query}
                onQueryChange={handleQueryChange}
                dates={dates}
                onDatesChange={handleDatesChange}
                onSearch={handleSearch}
            />

            {params?.query && (
                <Query endpoint="/publication/research/" params={params}>
                    <SearchResult
                        onSelectTag={handleSelectTag}
                        downloadURL={`/api/publication/ris/?${searchParams.toString()}`}
                    />
                </Query>
            )}
        </Page>
    );
};

export default SearchPage;
