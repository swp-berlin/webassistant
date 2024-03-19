import UpdatePublicationCount from './UpdatePublicationCount';

const LastPublicationCountUpdate = ({id, canManage, onMonitorUpdate, children}) => (
    canManage
        ? <UpdatePublicationCount id={id} onMonitorUpdate={onMonitorUpdate}>{children}</UpdatePublicationCount>
        : children
);

export default LastPublicationCountUpdate;
