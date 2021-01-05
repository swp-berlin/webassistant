import {useCallback} from 'react';
import {Button} from '@blueprintjs/core';
import {faRedo} from '@fortawesome/free-solid-svg-icons/faRedo';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';

import _ from 'utils/i18n';

const Label = _('Reload');

const ReloadButton = ({reload, ...props}) => {
    const handleClick = useCallback(
        event => {
            event.preventDefault();
            reload();
        },
        [reload],
    );

    return (<Button {...props} onClick={handleClick} />);
};

ReloadButton.defaultProps = {
    icon: (<FontAwesomeIcon icon={faRedo} />),
    text: Label,
};

export default ReloadButton;
