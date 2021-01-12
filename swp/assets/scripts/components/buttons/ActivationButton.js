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


const ActivationButton = ({endpoint, isActive, onToggle, disabled, ...props}) => {
    const history = useHistory();
    const [mutate, result] = useMutation(endpoint);

    const handleSubmit = useCallback(
        async (data, method = 'PATCH') => {
            const response = await mutate(data, method);
            handleMutationResult(response, {history});

            if (response.success) {
                onToggle(response.result.data.is_active);
            }
        },
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [mutate, history],
    );

    const onClick = () => handleSubmit({is_active: !isActive});

    const text = getLabel(isActive);
    return (
        <Button
            intent={Intent.PRIMARY}
            text={text}
            onClick={onClick}
            disabled={disabled || result.loading}
            {...props}
        />
    );
};

ActivationButton.propTypes = {
    endpoint: PropTypes.string.isRequired,
    isActive: PropTypes.bool.isRequired,
};

export default ActivationButton;
