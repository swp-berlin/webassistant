import {Button, Intent} from '@blueprintjs/core';
import {Link} from 'react-router-dom';
import {useBreadcrumb} from 'components/Navigation';
import PageHeading from 'components/PageHeading';

import _ from 'utils/i18n';

import ThinktankTable from './ThinktankTable';


const ThinktanksLabel = _('Thinktanks');
const NewLabel = _('New Thinktank');

const NewThinktankButton = (
    <Link to="/thinktank/new/">
        <Button intent={Intent.PRIMARY} text={NewLabel} />
    </Link>
);

const ThinktankList = () => {
    useBreadcrumb('/thinktank/', ThinktanksLabel);

    return (
        <div>
            <PageHeading
                title={ThinktanksLabel}
                actions={[NewThinktankButton]}
            />
            <ThinktankTable endpoint="thinktank" />
        </div>
    );
};

export default ThinktankList;
