import {TextArea} from 'components/forms';
import {isZoteroKey} from 'utils/validation';
import _, {interpolate} from 'utils/i18n';

const Label = _('Zotero Keys');
const HelpText = '{API_KEY}/(users|groups)/{USER_OR_GROUP_ID}/(items|collections|...)';
const InvalidKeysError = _('The following keys are invalid: %(keys)s');

const toKeyArray = value => value.trim().split('\n').filter(e => e.length);

const validate = keys => {
    const invalid = toKeyArray(keys).filter(key => !isZoteroKey(key));
    if (invalid.length) {
        return interpolate(InvalidKeysError, {keys: invalid});
    }

    return true;
};

const ZoteroKeysField = ({register, ...props}) => (
    <>
        <TextArea
            name="zotero_keys"
            register={register({
                required: false,
                validate,
                setValueAs: toKeyArray,
            })}
            label={Label}
            fill
            growVertically
            rows="5"
            {...props}
        />
        <div className="bp3-text-muted mb-5 -mt-2">
            {HelpText}
        </div>
    </>
);

export default ZoteroKeysField;
