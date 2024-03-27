import {Spinner, SpinnerSize} from '@blueprintjs/core';

import Query from 'components/Query';

const SmallSpinner = () => <Spinner className="justify-start" size={SpinnerSize.SMALL} />;

const Components = {
    idle: SmallSpinner,
    loading: SmallSpinner,
};

const MonitorTransferredCount = ({id}) => (
    <Query queryKey={['monitor', id, 'transferred-count']} components={Components}>
        {({transferred_count: transferredCount}) => transferredCount === null ? '—' : transferredCount}
    </Query>
);

export default MonitorTransferredCount;
