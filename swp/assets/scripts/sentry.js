/* eslint-disable no-console */

import {init, configureScope, captureMessage, captureException} from '@sentry/react';

const Sentry = window.Sentry = {
    environment: window.SentryEnvironment,
    release: window.SentryRelease,
};

if (process.env.NODE_ENV === 'production') {
    init({...Sentry, dsn: 'https://04f945b1a9fd4c7786c28b3913822b1f@sentry.cosmocode.de/40'});

    const user = window.SentryUserData ? {...window.SentryUserData} : null;

    if (user) configureScope(scope => scope.setUser(user));

    Sentry.message = captureMessage;
    Sentry.exception = captureException;
} else {
    Sentry.message = message => console.log(message);
    Sentry.exception = exception => console.error(exception);
}
