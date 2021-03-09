import {AnchorButton} from '@blueprintjs/core';
import _ from 'utils/i18n';


const DownloadLabel = _('Download .RIS');

const DownloadButton = ({href, ...props}) => (
    <AnchorButton
        minimal
        download
        icon="download"
        text={DownloadLabel}
        href={href}
        {...props}
    />
);

export default DownloadButton;
