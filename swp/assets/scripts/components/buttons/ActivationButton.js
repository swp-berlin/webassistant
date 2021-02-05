import {useCallback, useEffect} from 'react';
import PropTypes from 'prop-types';
import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {useMutationResult} from 'components/Fetch/Form';
import {useControllableState} from 'hooks/state';


const ActivateLabel = _('Activate');
const DeactivateLabel = _('Deactivate');
const DefaultActivatedMessage = _('Sucessfully activated');
const DefaultDeactivatedMessage = _('Sucessfully deactivated');

const getLabel = isActive => (isActive ? DeactivateLabel : ActivateLabel);


const ActivationButton = props => {
    const {
        endpoint, mutationOptions,
        isActiveKey, isActive: isActiveProvided, onToggle, defaultIsActive,
        disabled,
        activatedMessage,
        deactivatedMessage,
        ...other
    } = props;

    const [isActive, setIsActive] = useControllableState({
        value: isActiveProvided,
        onChange: onToggle,
        defaultValue: defaultIsActive,
    });
    const [handleSubmit, mutationResult] = useMutationResult(
        endpoint,
        {
            handleSuccess: ({is_active: isActive}) => ({
                intent: 'success',
                message: isActive ? activatedMessage : deactivatedMessage,
            }),
            ...mutationOptions,
        },
        [],
    );
    const {loading, result: {data}, success} = mutationResult;

    useEffect(() => {
        if (success) setIsActive(data[isActiveKey]);
    }, [success, data, setIsActive, isActiveKey]);

    const handleClick = useCallback(
        () => handleSubmit({[isActiveKey]: !isActive}, 'PATCH'),
        [handleSubmit, isActiveKey, isActive],
    );

    const text = getLabel(isActive);
    return (
        <Button
            intent={Intent.PRIMARY}
            text={text}
            onClick={handleClick}
            disabled={disabled || loading}
            {...other}
        />
    );
};

ActivationButton.propTypes = {
    isActiveKey: PropTypes.string,
    endpoint: PropTypes.string.isRequired,
    isActive: PropTypes.bool,
    activatedMessage: PropTypes.string,
    deactivatedMessage: PropTypes.string,
};

ActivationButton.defaultProps = {
    isActive: undefined,
    isActiveKey: 'is_active',
    activatedMessage: DefaultActivatedMessage,
    deactivatedMessage: DefaultDeactivatedMessage,
};

export default ActivationButton;
