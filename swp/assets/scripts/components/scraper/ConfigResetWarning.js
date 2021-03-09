import {Button, Classes, Dialog} from '@blueprintjs/core';

import _ from 'utils/i18n';


const Title = _('Warning');
const Warning = _('Changing the scraper type will reset the scraper configuration. Do you want to proceed?');
const AbortLabel = _('Abort');
const ProceedLabel = _('Proceed');

const ConfigResetWarning = ({isOpen, onAbort, onConfirm}) => (
    <Dialog title={Title} icon="warning-sign" isOpen={isOpen} onClose={onAbort}>
        <div className={Classes.DIALOG_BODY}>
            {Warning}
        </div>
        <div className={Classes.DIALOG_FOOTER}>
            <div className={Classes.DIALOG_FOOTER_ACTIONS}>
                <Button text={AbortLabel} onClick={onAbort} />
                <Button intent="danger" text={ProceedLabel} onClick={onConfirm} />
            </div>
        </div>
    </Dialog>
);

export default ConfigResetWarning;
