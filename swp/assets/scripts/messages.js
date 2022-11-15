import _, {interpolate} from 'utils/i18n';

export const NetworkError = _('A network error occurred. Please try again.');
export const ServerError = _('Something went wrong on our side…');
export const Maintenance = _('We are currently doing maintenance work. Please try again in a few seconds.');

const Generic = _('An error occurred: %(error)s');

export const getGenericErrorMessage = error => interpolate(Generic, {error});
