import PropTypes from 'prop-types';

import {MonitorPreview} from 'components/monitor';
import {getThinktankFilterDownloadURL} from './helper';

const ThinktankFilterPreview = ({id, monitorID, onlyNew, downloadURL, ...props}) => (
    <MonitorPreview
        id={monitorID}
        thinktankFilterID={id}
        onlyNew={onlyNew}
        downloadURL={downloadURL || getThinktankFilterDownloadURL(id, monitorID, onlyNew)}
        {...props}
    />
);

ThinktankFilterPreview.defaultProps = {
    onlyNew: false,
    downloadURL: '',
};

ThinktankFilterPreview.propTypes = {
    id: PropTypes.number.isRequired,
    monitorID: PropTypes.number.isRequired,
    onlyNew: PropTypes.bool,
    downloadURL: PropTypes.string,
};

export default ThinktankFilterPreview;
