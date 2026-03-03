import _, {interpolate} from 'utils/i18n';


const ThinktankLabel = _('Thinktank %s');

export const getThinktankLabel = (id, {result: {data}, loading}) => (
    loading || !data ? interpolate(ThinktankLabel, [id], false) : data.name
);
