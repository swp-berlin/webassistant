import {useEffect, useMemo} from 'react';

import {useFetch} from 'hooks/query';
import {interpolate} from 'utils/i18n';
import {buildURL} from 'utils/url';
import {Result} from 'components/Fetch';
import MarkDown from 'components/MarkDown';


const Snippet = ({source, context, ...props}) => {
    const content = useMemo(() => (source && context ? interpolate(source, context) : source), [source, context]);

    return <MarkDown {...props} source={content} />;
};

const RemoteSnippet = ({identifier, context, children, notFound, ...props}) => {
    const url = buildURL('snippet', identifier);
    const [fetch, result] = useFetch(url);

    useEffect(() => { fetch(); }, [fetch]);

    return (
        <Result
            result={result}
            handleClientError={notFound}
        >
            {source => <Snippet source={source} context={context} {...props} />}
        </Result>
    );
};

export default RemoteSnippet;
