import {buildURL} from './url';

export const buildAPIURL = (endpoint, id = null, action = null, ...additional) => (
    buildURL('api', endpoint, id, action, ...additional)
);
