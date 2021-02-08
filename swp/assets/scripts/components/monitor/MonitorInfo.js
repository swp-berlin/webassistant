import DateTime from 'components/DateTime';
import {getLabel} from 'utils/choices';
import _ from 'utils/i18n';


const PublicationCountLabel = _('Publications overall:');
const NewPublicationsLabel = _('Publications since last email:');
const LastSentLabel = _('Email sent:');
const IntervalLabel = _('Interval:');
const RecipientsLabel = _('Recipients:');


const MonitorInfo = ({publicationCount, newPublicationCount, lastSent, interval, recipientCount, ...props}) => (
    <dl {...props}>
        <div className="mb-1 sm:grid sm:grid-cols-5 sm:gap-4">
            <dt>{PublicationCountLabel}</dt>
            <dd className="sm:col-span-4">
                {publicationCount}
            </dd>
        </div>

        <div className="mb-1 sm:grid sm:grid-cols-5 sm:gap-4">
            <dt>{NewPublicationsLabel}</dt>
            <dd className="sm:col-span-4">
                {newPublicationCount}
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

export default MonitorInfo;
