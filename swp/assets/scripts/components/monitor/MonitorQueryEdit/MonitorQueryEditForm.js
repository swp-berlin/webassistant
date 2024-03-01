import {useCallback, useState} from 'react';
import {useNavigate, useSearchParams} from 'react-router-dom';
import {Button, Intent, TextArea} from '@blueprintjs/core';

import {buildAPIURL} from 'utils/api';
import _, {interpolate} from 'utils/i18n';
import {showToast} from 'utils/toaster';
import {getClientErrors} from 'utils/react-query-fetch';

import {useMutation} from 'hooks/react-query';

import Field from 'components/forms/Field';
import SearchQuery from 'components/Search/SearchQuery';

import MonitorQueryResult from './MonitorQueryResult';

const SaveLabel = _('Save');
const SearchLabel = _('Search');
const SuccessMessage = _('Successfully changed query of monitor %(name)s.');

const usePage = () => {
    const [searchParams] = useSearchParams();

    let page = searchParams.get('page');

    if (page) {
        page = parseInt(page);

        return Number.isNaN(page) ? null : page;
    }

    return page;
};

const MonitorQueryEditForm = ({monitor}) => {
    const page = usePage();
    const navigate = useNavigate();
    const url = buildAPIURL('monitor', monitor.id);
    const [query, setQuery] = useState(monitor.query || '');
    const [searchQuery, setSearchQuery] = useState(query);
    const {mutate, error, isLoading} = useMutation(url, 'PATCH', {
        onSuccess(data) {
            showToast(interpolate(SuccessMessage, data));
            navigate(`/monitor/${data.id}/`);
        },
    });
    const clientErrors = getClientErrors(error);
    const handleQueryChange = useCallback(({target}) => setQuery(target.value), [setQuery]);
    const handleSearch = useCallback(
        event => {
            event.preventDefault();
            setSearchQuery(query);
        },
        [query, setSearchQuery],
    );
    const handleSave = useCallback(
        event => {
            handleSearch(event);
            mutate({query});
        },
        [query, handleSearch, mutate],
    );

    return (
        <div className="mt-4">
            <Field name="query" errors={clientErrors} required>
                <TextArea value={query} onChange={handleQueryChange} rows={3} growVertically fill />
            </Field>
            <div className="flex justify-between">
                <Button disabled={query.length < 3} onClick={handleSearch}>{SearchLabel}</Button>
                <Button intent={Intent.PRIMARY} loading={isLoading} onClick={handleSave}>{SaveLabel}</Button>
            </div>
            {searchQuery && (
                <SearchQuery query={searchQuery} page={page}>
                    <MonitorQueryResult page={page} />
                </SearchQuery>
            )}
        </div>
    );
};

export default MonitorQueryEditForm;
