import {useLocation} from 'react-router-dom';
import PropTypes from 'prop-types';

import _ from 'utils/i18n';

import {useQuery} from 'hooks/query';

import Page from 'components/Page';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import {PublicationPreview} from 'components/publication';

import {useMonitorsBreadcrumb} from './MonitorList';
import {useMonitorBreadcrumb} from './MonitorDetail';

const PublicationsLabel = _('Publications');
const NewPublicationsLabel = _('New Publications');

const MonitorPreview = ({id, thinktankFilterID, onlyNew, downloadURL, ...props}) => {
    const endpoint = `/monitor/${id}/`;
    const location = useLocation();
    const query = useQuery(endpoint);

    const label = onlyNew ? NewPublicationsLabel : PublicationsLabel;

    useMonitorsBreadcrumb();
    useMonitorBreadcrumb(endpoint, id, query.result.data);
    useBreadcrumb(location.pathname, label);

    return (
        <Result result={query}>
            {({name, description, last_sent: lastSent}) => (
                <Page title={name}>
                    <p className="abstract mt-4">
                        {description}
                    </p>

                    <PublicationPreview
                        monitorID={id}
                        thinktankFilterID={thinktankFilterID}
                        downloadURL={downloadURL}
                        since={onlyNew ? lastSent : null}
                        isActive
                        {...props}
                    />
                </Page>
            )}
        </Result>
    );
};

MonitorPreview.defaultProps = {
    thinktankFilterID: null,
    onlyNew: false,
};

MonitorPreview.propTypes = {
    id: PropTypes.number.isRequired,
    thinktankFilterID: PropTypes.number,
    onlyNew: PropTypes.bool,
    downloadURL: PropTypes.string.isRequired,
};

export default MonitorPreview;
