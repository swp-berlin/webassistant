import {useCallback, useEffect} from 'react';
import PropTypes from 'prop-types';
import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {useMutationResult} from 'components/Fetch/Form';


const ActivateLabel = _('Activate');
const DeactivateLabel = _('Deactivate');

const getLabel = isActive => (isActive ? DeactivateLabel : ActivateLabel);


const ActivationButton = ({endpoint, isActive, onToggle, disabled, ...props}) => {
    const [handleSubmit, mutationResult] = useMutationResult(endpoint, {}, []);
    const {loading, result: {data: thinktank}, success} = mutationResult;

    useEffect(() => {
        if (success) onToggle(thinktank.is_active);
    }, [success, thinktank, onToggle]);

    const handleClick = useCallback(
        () => handleSubmit({is_active: !isActive}, 'PATCH'),
        [isActive, handleSubmit],
    );

    const text = getLabel(isActive);
    return (
        <Button
            intent={Intent.PRIMARY}
            text={text}
            onClick={handleClick}
            disabled={disabled || loading}
            {...props}
        />
    );
};

ActivationButton.propTypes = {
    endpoint: PropTypes.string.isRequired,
    isActive: PropTypes.bool.isRequired,
};

export default ActivationButton;
