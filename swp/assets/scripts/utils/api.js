import {buildURL} from './url';

export const buildAPIURL = (endpoint, id = null, action = null) => buildURL('api', endpoint, id, action);
