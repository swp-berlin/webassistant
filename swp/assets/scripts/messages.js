import _, {interpolate} from 'utils/i18n';

export const NetworkError = _('A network error occurred. Please try again.');
export const ServerError = _('Something went wrong on our side…');
export const Maintenance = _('We are currently doing maintenance work. Please try again in a few seconds.');

export const HttpErrorMessages = {
    400: _('Please correct the errors below.'),
    401: _('You have to be logged in to make this request.'),
    403: _('You are not allowed to make this request.'),
    404: _('The data you wanted to change does not exist anymore.'),
    502: Maintenance,
    503: Maintenance,
};

const Generic = _('An error occurred: %(error)s');

export const getGenericErrorMessage = error => interpolate(Generic, {error});
