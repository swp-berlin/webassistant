import _ from 'utils/i18n';

import {TextInput} from 'components/forms';

const SelectorLabel = _('Selector');
const SelectorInvalidMessage = _('Please enter a valid css selector');

const isValidSelector = selector => {
    try {
        document.createDocumentFragment().querySelector(selector);
    } catch (SyntaxError) {
        return SelectorInvalidMessage;
    }

    return true;
};

const SelectorField = ({register, required, ...props}) => (
    <TextInput
        register={register({validate: {invalid: value => !required || isValidSelector(value)}})}
        {...props}
    />
);

SelectorField.defaultProps = {
    required: false,
    label: SelectorLabel,
};

export default SelectorField;
