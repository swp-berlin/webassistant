/* eslint-disable no-confusing-arrow */

export const gettext = window.gettext || (msgid => msgid);

export const pgettext = window.pgettext || ((context, msgid) => msgid);

export const interpolate = (fmt, obj, named = true) => (window.interpolate || gettext)(fmt, obj, named);

export const getFormat = window.get_format || (fmt => fmt);

export const ngettext = window.ngettext || ((singular, plural, count) => count === 1 ? singular : plural);

export const npgettext = window.npgettext || ((context, singular, plural, count) => count === 1 ? singular : plural);

export default gettext;
