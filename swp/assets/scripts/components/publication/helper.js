import {interpolate, ngettext} from 'utils/i18n';


export const getPublicationsLabel = count => interpolate(
    ngettext('%s Publication', '%s Publications', count), [count], false,
);

export const parsePageParam = search => +new URLSearchParams(search).get('page');

export const withPageParam = (search, page) => {
    const params = new URLSearchParams(search);
    params.set('page', page);

    return params.toString();
};
