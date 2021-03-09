import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import {Result} from 'components/Fetch';
import {useQuery} from 'hooks/query';
import _ from 'utils/i18n';

import ThinktankEditForm from './ThinktankEditForm';
import {useThinktanksBreadcrumb} from './ThinktankList';
import {getThinktankLabel} from './helper';


const Title = _('Edit Thinktank');

const ThinktankEdit = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const result = useQuery(endpoint);

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
