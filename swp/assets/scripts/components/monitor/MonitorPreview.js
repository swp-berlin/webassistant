import {useLocation} from 'react-router-dom';
import PropTypes from 'prop-types';

import {useQuery} from 'hooks/query';
import _ from 'utils/i18n';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import {PublicationPreview} from 'components/publication';

import {getMonitorLabel} from './helper';
import {useMonitorsBreadcrumb} from './MonitorList';


const PublicationsLabel = _('Publications');
const NewPublicationsLabel = _('New Publications');

const MonitorPreview = ({id, onlyNew, ...props}) => {
    const endpoint = `/monitor/${id}/`;
    const location = useLocation();
    const query = useQuery(endpoint);

    const label = onlyNew ? NewPublicationsLabel : PublicationsLabel;

    useMonitorsBreadcrumb();
    useBreadcrumb(endpoint, getMonitorLabel(id, query));
    useBreadcrumb(location.pathname, label);

    return (
        <Result result={query}>
            {({name, description, last_sent: lastSent}) => (
                <Page title={name}>
                    <p className="abstract mt-4">
                        {description}
                    </p>

                    <PublicationPreview monitorID={id} since={onlyNew && lastSent} isActive {...props} />
                </Page>
            )}
        </Result>
    );
};

MonitorPreview.defaultProps = {
    onlyNew: false,
};

MonitorPreview.propTypes = {
    id: PropTypes.number.isRequired,
    onlyNew: PropTypes.bool,
};

export default MonitorPreview;
