import _, {interpolate} from 'utils/i18n';

export const getMonitorLabel = (id, {result: {data}, loading}) => (
    loading || !data ? interpolate(_('Monitor %s'), [id], false) : data.name
);
