import {Button, Intent} from '@blueprintjs/core';

import {buildAPIURL} from 'utils/api';
import _ from 'utils/i18n';

import {Endpoint} from '../PublicationList';

const Label = _('Export');

const ExportButton = ({id}) => (
    <a href={buildAPIURL(Endpoint, id, 'export')}>
        <Button intent={Intent.PRIMARY} text={Label} />
    </a>
);

export default ExportButton;
