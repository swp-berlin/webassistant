import {useMutationResult} from 'components/Fetch';
import {useCallback} from 'react';
import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';

const Label = _('Sync with Zotero');
const SuccessMessage = _('Transfer to Zotero started. This might take a couple of minutes.');

const TransferToZoteroButton = ({id}) => {
    const [mutate, {loading}] = useMutationResult(
        `/monitor/${id}/transfer-to-zotero/`,
        {successMessage: SuccessMessage},
    );
    const handleClick = useCallback(() => mutate(), [mutate]);

    return <Button text={Label} onClick={handleClick} loading={loading} />;
};

export default TransferToZoteroButton;
