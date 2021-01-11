import {Button, Intent} from '@blueprintjs/core';
import {useBreadcrumb} from 'components/Navigation';
import PageHeading from 'components/PageHeading';

import _ from 'utils/i18n';

import ThinktankTable from './ThinktankTable';


const ThinktanksLabel = _('Thinktanks');
const NewLabel = _('New Thinktank');

const NewThinktankButton = (
    <Button intent={Intent.PRIMARY} text={NewLabel} />
);

const ThinktankList = () => {
    useBreadcrumb('/thinktank/', ThinktanksLabel);

    return (
        <main>
            <PageHeading
                title={ThinktanksLabel}
                actions={[NewThinktankButton]}
            />
            <ThinktankTable endpoint="thinktank" />
        </main>
    );
};

export default ThinktankList;
