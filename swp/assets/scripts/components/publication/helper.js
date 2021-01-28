import {interpolate, ngettext} from 'utils/i18n';


export const getPublicationsLabel = count => interpolate(
    ngettext('%s Publication', '%s Publications', count), [count], false,
);
