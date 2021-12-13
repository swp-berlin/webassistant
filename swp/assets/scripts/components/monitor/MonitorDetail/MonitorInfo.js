import DateTime from 'components/DateTime';
import {getLabel} from 'utils/choices';
import _ from 'utils/i18n';

import MonitorPublicationsLink from 'components/monitor/MonitorPublicationsLink';


const PublicationCountLabel = _('Publications overall:');
const NewPublicationsLabel = _('Publications since last email:');
const LastSentLabel = _('Email sent:');
const IntervalLabel = _('Interval:');
const RecipientsLabel = _('Recipients:');
const TransferredToZoteroLabel = _('Transferred to Zotero');

const MonitorInfo = props => {
    const {id, publicationCount, newPublicationCount, lastSent, interval, recipientCount, transferredCount} = props;

    return (
        <dl {...props}>
            <div className="mb-1 sm:grid sm:grid-cols-5 sm:gap-4">
                <dt>{PublicationCountLabel}</dt>
                <dd className="sm:col-span-4">
                    <MonitorPublicationsLink id={id}>
                        {publicationCount}
                    </MonitorPublicationsLink>
                </dd>
            </div>

            <div className="mb-1 sm:grid sm:grid-cols-5 sm:gap-4">
                <dt>{NewPublicationsLabel}</dt>
                <dd className="sm:col-span-4">
                    <MonitorPublicationsLink id={id} onlyNew>
                        {newPublicationCount}
                    </MonitorPublicationsLink>
                </dd>
            </div>

            <div className="mb-1 sm:grid sm:grid-cols-5 sm:gap-4">
                <dt>{TransferredToZoteroLabel}</dt>
                <dd className="sm:col-span-4">
                    {transferredCount}
                </dd>
            </div>

            <div className="mb-1 sm:grid sm:grid-cols-5 sm:gap-4">
                <dt>{LastSentLabel}</dt>
                <dd className="sm:col-span-4">
                    <DateTime value={lastSent} />
                </dd>
            </div>

            <div className="mb-1 sm:grid sm:grid-cols-5 sm:gap-4">
                <dt>{IntervalLabel}</dt>
                <dd className="sm:col-span-4">
                    {interval ? getLabel('interval', interval) : '—'}
                </dd>
            </div>

            <div className="sm:grid sm:grid-cols-5 sm:gap-4">
                <dt>{RecipientsLabel}</dt>
                <dd className="sm:col-span-4">
                    {recipientCount}
                </dd>
            </div>
        </dl>
    );
};

export default MonitorInfo;
