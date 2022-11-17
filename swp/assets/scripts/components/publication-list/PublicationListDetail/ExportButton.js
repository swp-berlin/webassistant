import {AnchorButton, Intent} from '@blueprintjs/core';

import {buildAPIURL} from 'utils/api';
import _ from 'utils/i18n';

import {Endpoint} from '../PublicationList';

const Label = _('Export');

const ExportButton = ({id}) => (
    <AnchorButton href={buildAPIURL(Endpoint, id, 'export')} intent={Intent.PRIMARY}>
        {Label}
    </AnchorButton>
);

export default ExportButton;
