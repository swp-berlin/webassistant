import {useCallback, useState} from 'react';
import {Link, useSearchParams} from 'react-router-dom';
import {Button, Intent} from '@blueprintjs/core';
import parseISO from 'date-fns/parseISO';
import formatISO from 'date-fns/formatISO';
import without from 'lodash/without';

import _ from 'utils/i18n';

import Page from 'components/Page';
import {useBreadcrumb} from 'components/Navigation';
import Query from 'components/Query';

import SearchForm from './SearchForm';
import SearchResult from './SearchResult';

const SearchLabel = _('Search');
const PublicationListLabel = _('Publication Lists');

const Actions = [
    <Link key={1} to="publication-list/">
        <Button intent={Intent.PRIMARY}>
            {PublicationListLabel}
        </Button>
    </Link>,
];

const formatDate = date => date && formatISO(date, {representation: 'date'});
const parseDate = date => (date ? parseISO(date) : null);

const WhitespaceRegEx = /\s/g;
const maybeQuote = text => {
    const hasWhiteSpace = WhitespaceRegEx.test(text);
    return hasWhiteSpace ? `"${text}"` : text;
};

const SearchPage = () => {
    useBreadcrumb('/search/', SearchLabel);
    const [searchParams, setSearchParams] = useSearchParams();

    const [term, setTerm] = useState(searchParams.get('query') || '');
    const handleTermChange = useCallback(term => setTerm(term), []);

    const [dates, setDates] = useState(
        () => [parseDate(searchParams.get('start_date')), parseDate(searchParams.get('end_date'))],
    );
    const handleDatesChange = useCallback(dates => {
        setDates(dates);
        setSearchParams(next => {
            const [startDate, endDate] = dates;
            if (startDate) {
                next.set('start_date', formatDate(startDate));
            } else next.delete('start_date');
            if (endDate) {
                next.set('end_date', formatDate(endDate));
            } else next.delete('end_date');
            return next;
        });
    }, [setSearchParams]);

    const query = searchParams.get('query');
    const tags = searchParams.getAll('tag');
    const startDate = searchParams.get('start_date');
    const endDate = searchParams.get('end_date');

    const handleSelectTag = useCallback(tag => {
        setSearchParams(next => {
            const tags = next.getAll('tag');
            if (tags.includes(tag)) {
                next.delete('tag');
                without(tags, tag).forEach(tag => next.append('tag', tag));
            } else {
                next.append('tag', tag);
            }

            return next;
        });
    }, [setSearchParams]);

    const handleSearch = useCallback(() => {
        setSearchParams(next => {
            next.delete('tag');
            if (term) {
                next.set('query', term);
            } else next.delete('term');
            return next;
        });
    }, [term, setSearchParams]);

    const addFilter = filter => {
        if (filter.field === 'tags') return handleSelectTag(filter.value);

        const query = searchParams.get('query');
        const filterString = `${filter.field}:${maybeQuote(filter.value)}`;

        if (!query.includes(filterString)) {
            setSearchParams(next => {
                next.set('query', `${filterString} ${next.get('query')}`);
                return next;
            });
            setTerm(term => `${filterString} ${term}`);
        }
    };

    const params = {};
    if (query) params.query = query;
    if (tags.length) params.tag = tags;
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;

    return (
        <Page title={SearchLabel} actions={Actions}>
            <SearchForm
                query={term}
                onQueryChange={handleTermChange}
                dates={dates}
                onDatesChange={handleDatesChange}
                onSearch={handleSearch}
            />

            {params.query && (
                <Query queryKey={['publication', 'research', params]}>
                    <SearchResult
                        selectedTags={tags}
                        onSelectTag={handleSelectTag}
                        downloadURL={`/api/publication/ris/?${searchParams.toString()}`}
                        onAddFilter={addFilter}
                    />
                </Query>
            )}
        </Page>
    );
};

export default SearchPage;
