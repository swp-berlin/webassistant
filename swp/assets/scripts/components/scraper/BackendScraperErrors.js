import {Callout, Intent} from '@blueprintjs/core';
import DateTime from 'components/DateTime';
import ExternalLink from 'components/Navigation/ExternalLink';
import {getPublicationFieldLabel} from 'components/publication/PublicationField';

import _, {interpolate} from 'utils/i18n';

const PublicationLabel = _('Publication %s');
const ErrorLabel = _('Error in ');
const FieldLabel = _('Field: %s');
const CodeLabel = _('Code: %s');

const groupByPublication = errors => (
    errors.reduce((results, {id, identifier, publication, message, field, code, level, timestamp}) => {
        if (level !== 'error') {
            return results;
        }

        const position = publication?.id || 0;
        if (!results[position]) {
            results[position] = [];
        }

        results[position].push({id, identifier, publication, message, field, code, level, timestamp});
        return results;
    }, {})
);


const GlobalErrors = ({errors}) => (
    <section className="global-errors mb-6">
        <ul className="list-none pl-0 space-y-2">
            {errors.map(({id, identifier, message, field, code, timestamp}) => (
                <li className="scraper-error" data-id={id} data-field={field} data-code={code}>
                    <Callout intent={Intent.DANGER} title={identifier}>
                        {timestamp && (
                            <p><small className="text-gray-400"><DateTime value={timestamp} /></small></p>
                        )}

                        <p className="whitespace-pre-line">
                            {field && <strong>{`${getPublicationFieldLabel(field)}: `}</strong>}
                            {message}
                        </p>
                    </Callout>
                </li>
            ))}
        </ul>
    </section>
);

const PublicationErrors = ({publicationID, errors}) => {
    const realErrors = errors.filter(error => error.level === 'error');
    const timestamp = realErrors.length && realErrors[0].timestamp;
    const publication = realErrors.length && realErrors[0].publication;
    const title = publication?.title;

    return (
        <section className="publication-errors" data-publication={publicationID}>
            <header>
                <h4 className="text-red-600">
                    <strong>{ErrorLabel}</strong>
                    {title ? <q>{title}</q> : interpolate(PublicationLabel, [publicationID], false)}
                </h4>
                {timestamp && <p><small className="text-gray-400"><DateTime value={timestamp} /></small></p>}
                <div>
                    <ExternalLink to={publication.url}>{publication.url}</ExternalLink>
                </div>
            </header>
            <ul className="mt-2">
                {realErrors.map(({id, message, field, code}) => (
                    <li className="scraper-error" data-id={id}>
                        <div>
                            <ul className="list-none pl-0 mb-0">
                                {field && (
                                    <li>
                                        <strong>{interpolate(FieldLabel, [field], false)}</strong>
                                    </li>
                                )}
                                {code && (
                                    <li>
                                        <strong>{interpolate(CodeLabel, [code], false)}</strong>
                                    </li>
                                )}
                            </ul>
                            <p>{message}</p>
                        </div>
                    </li>
                ))}
            </ul>
        </section>
    );
};

const BackendScraperErrors = ({errors}) => {
    const publicationErrors = groupByPublication(errors);
    const entries = Object.entries(publicationErrors);
    const [, globalErrors] = entries.length && entries.shift();

    return (
        <div className="backend-errors mt-6 space-y-3">
            {globalErrors && <GlobalErrors errors={globalErrors} />}
            {entries.length > 0 && entries.map(
                ([id, errors]) => <PublicationErrors publicationID={id} errors={errors} />,
            )}
        </div>
    );
};

BackendScraperErrors.defaultProps = {
    errors: [],
};

export default BackendScraperErrors;
