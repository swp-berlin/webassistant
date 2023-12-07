import {useCallback, useMemo, useRef, useState} from 'react';
import {Link, useSearchParams} from 'react-router-dom';
import {AnchorButton, Button, Intent} from '@blueprintjs/core';
import parseISO from 'date-fns/parseISO';
import formatISO from 'date-fns/formatISO';

import _ from 'utils/i18n';

import Page from 'components/Page';
import {useBreadcrumb} from 'components/Navigation';

import SearchForm from './SearchForm';
import SearchQuery from './SearchQuery';
import SearchResult from './SearchResult';

import HelpTextFileURL from './helptext.pdf';

const HelpLabel = _('Help');
const SearchLabel = _('Search');
const PublicationListLabel = _('Publication Lists');

const Actions = [
    <Link key={1} to="publication-list/">
        <Button intent={Intent.PRIMARY}>
            {PublicationListLabel}
        </Button>
    </Link>,
    <AnchorButton
        key={2}
        href={HelpTextFileURL}
        text="?"
        intent={Intent.NONE}
        target="blank"
        title={HelpLabel}
        download
    />,
];

const updateParam = (searchParams, key, value) => {
    if (value) searchParams.set(key, value);
    else searchParams.delete(key);
};

const formatDate = date => date && formatISO(date, {representation: 'date'});
const parseDate = date => (date ? parseISO(date) : null);
const updateDate = (searchParams, key, value) => updateParam(searchParams, key, formatDate(value));

const useInitialDates = (startDate, endDate) => {
    const initialDates = useRef(null);

    if (initialDates.current === null) initialDates.current = [startDate, endDate].map(parseDate);

    return initialDates.current;
};

const removeFilterTerm = (query, filterTerm) => query.split(' ').filter(term => term !== filterTerm).join(' ');
const addFilterTerm = (query, filterTerm) => query ? `${query} ${filterTerm}` : filterTerm;

const Quote = '"';
const WhitespaceRegEx = /\s/g;
const maybeQuote = text => WhitespaceRegEx.test(text) ? `${Quote}${text}${Quote}` : text;
const maybeUnquote = text => (
    text.startsWith(Quote) && text.endsWith(Quote)
        ? text.slice(Quote.length, -Quote.length)
        : text
);

const parseTags = query => (
    query
        .split(' ')
        .filter(term => term.startsWith('tags:'))
        .map(term => {
            const [, tag] = term.split(':');

            return maybeUnquote(tag);
        })
);

const SearchPage = () => {
    useBreadcrumb('/search/', SearchLabel);

    const [searchParams, setSearchParams] = useSearchParams();

    const query = searchParams.get('query');
    const startDate = searchParams.get('start_date');
    const endDate = searchParams.get('end_date');
    const page = searchParams.get('page');

    const [term, setTerm] = useState(query || '');
    const handleTermChange = useCallback(term => setTerm(term), []);

    const initialDates = useInitialDates(startDate, endDate);
    const handleDatesChange = useCallback(([startDate, endDate]) => {
        setSearchParams(next => {
            updateDate(next, 'start_date', startDate);
            updateDate(next, 'end_date', endDate);

            next.delete('page');

            return next;
        });
    }, [setSearchParams]);

    const handleSearch = useCallback(() => {
        setSearchParams(next => {
            updateParam(next, 'query', term);

            if (term !== query) next.delete('page');

            return next;
        });
    }, [setSearchParams, term, query]);

    const addFilter = useCallback(filter => {
        const query = searchParams.get('query') || '';
        const filterTerm = `${filter.field}:${maybeQuote(filter.value)}`;
        const toggle = query.includes(filterTerm) ? removeFilterTerm : addFilterTerm;

        setSearchParams(next => {
            const query = next.get('query');

            next.set('query', toggle(query, filterTerm));

            return next;
        });
        setTerm(term => toggle(term, filterTerm));
    }, [searchParams, setSearchParams]);

    const handleSelectTag = useCallback(tag => addFilter({field: 'tags', value: tag}), [addFilter]);

    const tags = useMemo(() => parseTags(query || ''), [query]);

    return (
        <Page title={SearchLabel} actions={Actions}>
            <SearchForm
                query={term}
                initialDates={initialDates}
                onQueryChange={handleTermChange}
                onDatesChange={handleDatesChange}
                onSearch={handleSearch}
            />

            {query && (
                <SearchQuery query={query} startDate={startDate} endDate={endDate} page={page}>
                    <SearchResult
                        selectedTags={tags}
                        onSelectTag={handleSelectTag}
                        downloadURL={`/api/publication/ris/?${searchParams.toString()}`}
                        onAddFilter={addFilter}
                    />
                </SearchQuery>
            )}
        </Page>
    );
};

export default SearchPage;
