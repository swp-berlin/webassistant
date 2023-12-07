import {useCallback, useState} from 'react';
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
    const query = searchParams.get('query');

    const [term, setTerm] = useState(query || '');
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
            next.delete('page');
            return next;
        });
    }, [setSearchParams]);

    const tags = searchParams.getAll('tag');
    const startDate = searchParams.get('start_date');
    const endDate = searchParams.get('end_date');
    const page = searchParams.get('page');

    const handleSearch = useCallback(() => {
        setSearchParams(next => {
            next.delete('tag');
            if (term) {
                next.set('query', term);
            } else next.delete('query');

            if (term !== query) next.delete('page');
            return next;
        });
    }, [setSearchParams, term, query]);

    const addFilter = useCallback(filter => {
        const query = searchParams.get('query');
        const filterString = `${filter.field}:${maybeQuote(filter.value)}`;

        if (!query.includes(filterString)) {
            setSearchParams(next => {
                next.set('query', `${next.get('query')} ${filterString}`);
                return next;
            });
            setTerm(term => `${term} ${filterString}`);
        }
    }, [searchParams, setSearchParams]);

    const handleSelectTag = useCallback(tag => addFilter({field: 'tags', value: tag}), [addFilter]);

    return (
        <Page title={SearchLabel} actions={Actions}>
            <SearchForm
                query={term}
                onQueryChange={handleTermChange}
                dates={dates}
                onDatesChange={handleDatesChange}
                onSearch={handleSearch}
            />

            {query && (
                <SearchQuery query={query} tags={tags} startDate={startDate} endDate={endDate} page={page}>
                    <SearchResult
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
