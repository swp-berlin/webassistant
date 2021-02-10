import {AnchorButton} from '@blueprintjs/core';
import _ from 'utils/i18n';


const DownloadLabel = _('Download .RIS');

const DownloadButton = ({thinktankID, ...props}) => (
    <AnchorButton
        minimal
        download
        icon="download"
        text={DownloadLabel}
        href={`/thinktank/${thinktankID}/download/`}
        {...props}
    />
);

export default DownloadButton;
