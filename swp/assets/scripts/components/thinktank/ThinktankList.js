import {Button, Intent} from '@blueprintjs/core';
import {useBreadcrumb} from 'components/Navigation';
import PageHeading from 'components/PageHeading';

import _ from 'utils/i18n';

import ThinktankTable from './ThinktankTable';


const ThinktanksLabel = _('Thinktanks');
const NewLabel = _('New thinktank');

const ThinktankList = () => {
    useBreadcrumb('/thinktank/', ThinktanksLabel);

    return (
        <div>
            <PageHeading
                title={ThinktanksLabel}
                actions={[<Button intent={Intent.PRIMARY} text={NewLabel} />]}
            />
            <ThinktankTable endpoint="thinktank" />
        </div>
    );
};

export default ThinktankList;
