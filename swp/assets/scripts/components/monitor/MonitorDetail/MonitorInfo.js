import _ from 'utils/i18n';
import {getLabel} from 'utils/choices';

import DateTime from 'components/DateTime';
import MonitorPublicationsLink from 'components/monitor/MonitorPublicationsLink';

import LastPublicationCountUpdate from './LastPublicationCount';
import MonitorTransferredCount from './MonitorTransferredCount';

const PublicationCountLabel = _('Publications overall:');
const NewPublicationsLabel = _('Publications since last email:');
const LastPublicationCountUpdateLabel = _('Last update of publication count:');
const LastSentLabel = _('Email sent:');
const IntervalLabel = _('Interval:');
const RecipientsLabel = _('Recipients:');
const TransferredToZoteroLabel = _('Transferred to Zotero');

const MonitorInfo = props => {
    const {
        id,
        canManage,
        publicationCount,
        newPublicationCount,
        lastPublicationCountUpdate,
        lastSent,
        interval,
        recipientCount,
        onMonitorUpdate,
        ...other
    } = props;

    return (
        <dl id={id} {...other}>
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
                <dt>{LastPublicationCountUpdateLabel}</dt>
                <dd className="sm:col-span-4">
                    <LastPublicationCountUpdate id={id} canManage={canManage} onMonitorUpdate={onMonitorUpdate}>
                        <DateTime value={lastPublicationCountUpdate} />
                    </LastPublicationCountUpdate>
                </dd>
            </div>

            <div className="mb-1 sm:grid sm:grid-cols-5 sm:gap-4">
                <dt>{TransferredToZoteroLabel}</dt>
                <dd className="sm:col-span-4">
                    <MonitorTransferredCount id={id} />
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
