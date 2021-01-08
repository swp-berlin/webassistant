import {useCallback} from 'react';
import {useHistory} from 'react-router-dom';
import PropTypes from 'prop-types';

import {Button, Intent} from '@blueprintjs/core';
import _ from 'utils/i18n';
import {useMutation} from 'hooks/query';
import {handleMutationResult} from 'components/Fetch/Form';


const ActivateLabel = _('Activate');
const DeactivateLabel = _('Deactivate');

const getLabel = isActive => (isActive ? DeactivateLabel : ActivateLabel);


const ActivationButton = ({endpoint, isActive, ...props}) => {
    const history = useHistory();
    const [mutate, result] = useMutation(endpoint);

    const handleSubmit = useCallback(
        async (data, method = 'PATCH') => handleMutationResult(
            await mutate(data, method),
            {history},
        ),
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [mutate, history],
    );

    const onClick = () => handleSubmit({is_active: !isActive});
    console.log(result); // FIXME: How do I result?

    const text = getLabel(isActive);
    return <Button intent={Intent.PRIMARY} text={text} {...props} onClick={onClick} />;
};

ActivationButton.propTypes = {
    endpoint: PropTypes.string.isRequired,
    isActive: PropTypes.bool.isRequired,
};

export default ActivationButton;
