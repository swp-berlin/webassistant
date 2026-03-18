import {useParams} from 'react-router-dom';

import _ from 'utils/i18n';

import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import {usePoolBreadcrumb} from 'components/PoolBreadcrumb';
import {Result} from 'components/Fetch';

import {useQuery} from 'hooks/query';

import ThinktankEditForm from './ThinktankEditForm';
import {useThinktanksBreadcrumb} from './ThinktankList';
import {getThinktankLabel} from './helper';

const Title = _('Edit Thinktank');

const ThinktankEdit = props => {
    const {id} = useParams();
    const endpoint = `/thinktank/${id}/`;
    const result = useQuery(endpoint);

    usePoolBreadcrumb(result.result.data);
    useThinktanksBreadcrumb();
    useBreadcrumb(endpoint, getThinktankLabel(id, result));

    return (
        <Page title={Title}>
            <Result result={result}>
                {thinktank => (
                    <ThinktankEditForm
                        endpoint={endpoint}
                        data={thinktank}
                        backURL={endpoint}
                        {...props}
                    />
                )}
            </Result>
        </Page>
    );
};

export default ThinktankEdit;
