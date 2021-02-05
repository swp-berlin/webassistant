import _, {interpolate} from 'utils/i18n';


export const getMonitorLabel = (id, result = null) => (
    !result.data || result.loading ? interpolate(_('Monitor %s'), [id], false) : result.result.data.name
);
