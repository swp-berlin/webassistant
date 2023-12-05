import {Button, Intent} from '@blueprintjs/core';
import {Link} from 'react-router-dom';

import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _ from 'utils/i18n';

import ThinktankTable from './ThinktankTable';
import {usePoolSelect} from './PoolSelect';

const ThinktanksLabel = _('Thinktanks');
const NewLabel = _('New Thinktank');

export const useThinktanksBreadcrumb = (href = '/thinktank/', text = ThinktanksLabel) => (
    useBreadcrumb(href, text)
);

const ThinktankAddButton = ({...props}) => (
    <Link to="/thinktank/add/">
        <Button intent={Intent.PRIMARY} text={NewLabel} {...props} />
    </Link>
);

const ThinktankList = () => {
    useBreadcrumb('/thinktank/', ThinktanksLabel);

    const [pool, poolSelect] = usePoolSelect();
    const actions = (
        <>
            {poolSelect}
            <ThinktankAddButton />
        </>
    );

    return (
        <Page title={ThinktanksLabel} actions={actions}>
            <ThinktankTable endpoint="thinktank" pool={pool} />
        </Page>
    );
};

export default ThinktankList;
