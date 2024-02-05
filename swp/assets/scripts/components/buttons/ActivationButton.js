import {useCallback, useEffect} from 'react';
import PropTypes from 'prop-types';
import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {showToast} from 'utils/toaster';

import {useControllableState} from 'hooks/state';

import {DefaultHandlers, useMutationResult} from 'components/Fetch/Form';

const ActivateLabel = _('Activate');
const DeactivateLabel = _('Deactivate');
const DefaultActivatedMessage = _('Successfully activated');
const DefaultDeactivatedMessage = _('Successfully deactivated');

export const ActivationButton = ({isActive, intent = Intent.PRIMARY, ...props}) => (
    <Button intent={intent} text={isActive ? DeactivateLabel : ActivateLabel} {...props} />
);

const getMutationOptions = (mutationOptions, onToggle, activatedMessage, deactivatedMessage) => ({
    ...mutationOptions,
    handleSuccess(data, ...args) {
        const {is_active: isActive} = data;

        if (onToggle) onToggle(isActive);
        if (mutationOptions.handleSuccess) mutationOptions.handleSuccess(data, ...args);

        return ({
            intent: Intent.SUCCESS,
            message: isActive ? activatedMessage : deactivatedMessage,
        });
    },
    handleClientError(status, errors, ...args) {
        if (mutationOptions.handleClientError) return mutationOptions.handleClientError(status, errors, ...args);

        if (status === 400 && errors) {
            return Object.values(errors).forEach(messages => {
                messages.forEach(message => {
                    showToast(message, Intent.DANGER);
                });
            });
        }

        return DefaultHandlers.handleClientError(status, errors, ...args);
    },
});

const ActivationButtonController = props => {
    const {
        endpoint,
        mutationOptions = {},
        isActiveKey,
        isActive: isActiveProvided,
        defaultIsActive,
        onToggle,
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
        getMutationOptions(mutationOptions, onToggle, activatedMessage, deactivatedMessage),
        [activatedMessage, deactivatedMessage, onToggle],
    );

    const {loading, result: {data}, success} = mutationResult;

    useEffect(() => {
        if (success && setIsActive) setIsActive(data[isActiveKey]);
    }, [success, data, setIsActive, isActiveKey]);

    const handleClick = useCallback(
        () => handleSubmit({[isActiveKey]: !isActive}, 'PATCH'),
        [handleSubmit, isActiveKey, isActive],
    );

    return (
        <ActivationButton
            isActive={isActive}
            onClick={handleClick}
            disabled={disabled}
            loading={loading}
            {...other}
        />
    );
};

ActivationButtonController.propTypes = {
    isActiveKey: PropTypes.string,
    endpoint: PropTypes.string.isRequired,
    isActive: PropTypes.bool,
    activatedMessage: PropTypes.string,
    deactivatedMessage: PropTypes.string,
};

ActivationButtonController.defaultProps = {
    isActive: undefined,
    isActiveKey: 'is_active',
    activatedMessage: DefaultActivatedMessage,
    deactivatedMessage: DefaultDeactivatedMessage,
};

export default ActivationButtonController;
