import {useCallback, useEffect, useRef} from 'react';

import _ from 'utils/i18n';
import {useQuery} from 'hooks/query';
import {Result} from 'components/Fetch';

import {Status} from './common';
import PreviewResult from './PreviewResult';


const LoadingProps = {
    title: _('Loading Preview'),
    description: _('The Scraper is collecting publications. This may take a while.'),
};


const Preview = ({id}) => {
    const result = useQuery(`/preview/${id}/`);
    const {result: {data}, success, fetch} = result;
    const intervalRef = useRef();

    const refetch = useCallback(() => {
        fetch();
        intervalRef.current = setInterval(fetch, 5000);
    }, [fetch]);

    useEffect(() => {
        intervalRef.current = setInterval(fetch, 5000);
        return () => clearInterval(intervalRef.current);
    }, [fetch]);

    useEffect(() => {
        const requestFailed = !result.loading && !success;
        const taskEnded = data && data.status !== Status.Pending;

        if (requestFailed || taskEnded) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
    }, [data, result.loading, success]);

    const loading = result.loading || (success && data.status === Status.Pending);

    return (
        <div className="mt-6">
            <Result
                result={{...result, loading, fetch: refetch}}
                loadingProps={LoadingProps}
            >
                <PreviewResult />
            </Result>
        </div>
    );
};

export default Preview;
