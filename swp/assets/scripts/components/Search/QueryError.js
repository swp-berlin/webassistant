import ClientError from 'components/Fetch/ClientError';

import _ from 'utils/i18n';
import {AnchorButton} from '@blueprintjs/core';
import GenericErrorComponent from 'components/Query/GenericError';


const ErrorTitle = _('Invalid Query');
const DocsHref = 'https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax';
const DocsLabel = _('visit query syntax documentation');

const QueryError = ({error, query}) => {
    const {error: {data: {code, detail}}} = query;
    if (code !== 'invalid-query') return <GenericErrorComponent error={error} />;

    return (
        <ClientError
            action={<AnchorButton href={DocsHref} target="_blank" text={DocsLabel} title={DocsLabel} />}
            title={ErrorTitle}
            description={detail}
        />
    );
};

export default QueryError;
