import Field from 'components/forms/Field';
import {TextArea} from '@blueprintjs/core';
import {SearchButton} from 'components/Search/SearchForm';
import SearchQuery from 'components/Search/SearchQuery';
import MonitorQueryResult from 'components/monitor/MonitorQueryEdit/MonitorQueryResult';
import {Fragment, useState} from 'react';

const MonitorQueryBuilder = ({defaultValue}) => {
    const [quer, setValue] = useState(monitor.query || '');

    return (
        <Fragment>
            <form className={} onSubmit={handleSubmit}>
                <Field name="query" errors={clientErrors} required>
                    <TextArea value={query} onChange={handleQueryChange} rows={3} growVertically fill />
                </Field>
                <SearchButton disabled={query.length < 3} />
            </form>
            {searchQuery && (
                <SearchQuery query={searchQuery} pools={pools} page={page}>
                    <MonitorQueryResult page={page} />
                </SearchQuery>
            )}
        </Fragment>
    );
};
