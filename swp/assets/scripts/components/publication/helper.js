import _, {interpolate, ngettext} from 'utils/i18n';


const PublicationLabel = _('%s Publication');
const PublicationsLabel = _('%s Publications');

export const getPublicationsLabel = count => interpolate(
    ngettext(PublicationLabel, PublicationsLabel, count), [count], false,
);
