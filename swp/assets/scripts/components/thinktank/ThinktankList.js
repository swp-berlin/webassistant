import {Button, Intent} from '@blueprintjs/core';
import {Link} from 'react-router-dom';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';

import _ from 'utils/i18n';

import ThinktankTable from './ThinktankTable';


const ThinktanksLabel = _('Thinktanks');
const NewLabel = _('New Thinktank');

export const useThinktanksBreadcrumb = (href = '/thinktank/', text = ThinktanksLabel) => (
    useBreadcrumb(href, text)
);

const NewThinktankButton = (
    <Link to="/thinktank/new/">
        <Button intent={Intent.PRIMARY} text={NewLabel} />
    </Link>
);

const ThinktankList = () => {
    useBreadcrumb('/thinktank/', ThinktanksLabel);

    return (
        <Page title={ThinktanksLabel} actions={[NewThinktankButton]}>
            <ThinktankTable endpoint="thinktank" />
        </Page>
    );
};

export default ThinktankList;
