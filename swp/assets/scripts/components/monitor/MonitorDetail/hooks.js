import _, {interpolate} from 'utils/i18n';

import {useBreadcrumb} from 'components/Navigation';

const PoolLabel = _('Pool');
const FallbackLabel = _('Monitor %s');

const getFallbackLabel = id => interpolate(FallbackLabel, [id], false);

export const useMonitorBreadcrumb = (url, id, data) => {
    useBreadcrumb(null, data && data.pool ? data.pool.name : PoolLabel);
    useBreadcrumb(url, data ? data.name : getFallbackLabel(id));
};
