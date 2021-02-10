import {TextArea} from 'components/forms';
import {isEmail} from 'utils/validation';
import _, {interpolate} from 'utils/i18n';

const RecipientsLabel = _('Recipients');
const InvalidEmailError = _('Recipients must be valid email addresses: %(addresses)s');

const setValueAs = value => value.trim().split('\n').filter(e => e.length);

const validate = recipients => {
    const invalid = [];

    recipients.forEach(email => {
        if (!isEmail(email)) {
            invalid.push(email);
        }
    });

    if (invalid.length) return interpolate(InvalidEmailError, {addresses: invalid});

    return true;
};

const RecipientField = ({register, ...props}) => (
    <TextArea
        name="recipients"
        register={register({
            required: false,
            validate,
            setValueAs,
        })}
        label={RecipientsLabel}
        fill
        growVertically
        rows="5"
        {...props}
    />
);

export default RecipientField;
