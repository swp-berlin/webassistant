import {Button, Intent} from '@blueprintjs/core';
import {Link} from 'react-router-dom';

import {useBreadcrumb} from 'components/Navigation';
import {usePoolBreadcrumb} from 'components/PoolBreadcrumb';
import {usePoolSelect} from 'components/PoolSelect';
import Page from 'components/Page';

import _ from 'utils/i18n';
import {buildURL, withParams} from 'utils/url';

import ThinktankTable from './ThinktankTable';

const ThinktanksLabel = _('Thinktanks');
const NewLabel = _('New Thinktank');

export const useThinktanksBreadcrumb = (href = '/thinktank/', text = ThinktanksLabel) => (
    useBreadcrumb(href, text)
);

const ThinktankAddURL = buildURL('thinktank', 'add');

const getAddURL = pool => typeof pool === 'number' ? withParams(ThinktankAddURL, {pool}) : ThinktankAddURL;

const ThinktankAddButton = ({pool, ...props}) => (
    <Link to={getAddURL(pool)}>
        <Button intent={Intent.PRIMARY} text={NewLabel} {...props} />
    </Link>
);

const ThinktankList = () => {
    const [pool, poolSelect] = usePoolSelect();
    const actions = (
        <>
            {poolSelect}
            <ThinktankAddButton pool={pool} />
        </>
    );

    usePoolBreadcrumb(pool === null ? 'all' : pool);
    useBreadcrumb('/thinktank/', ThinktanksLabel);

    return (
        <Page title={ThinktanksLabel} actions={actions}>
            <ThinktankTable endpoint="thinktank" pool={pool} />
        </Page>
    );
};

export default ThinktankList;
