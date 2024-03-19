import {Button, Intent} from '@blueprintjs/core';
import {Link} from 'react-router-dom';

import {useBreadcrumb} from 'components/Navigation';
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
    useBreadcrumb('/thinktank/', ThinktanksLabel);

    const [pool, poolSelect] = usePoolSelect();
    const actions = (
        <>
            {poolSelect}
            <ThinktankAddButton pool={pool} />
        </>
    );

    return (
        <Page title={ThinktanksLabel} actions={actions}>
            <ThinktankTable endpoint="thinktank" pool={pool} />
        </Page>
    );
};

export default ThinktankList;
