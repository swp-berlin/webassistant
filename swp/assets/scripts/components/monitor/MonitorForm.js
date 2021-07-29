import {Button, Intent} from '@blueprintjs/core';
import {useMutationForm} from 'components/Fetch';
import {Select, TextArea, TextInput} from 'components/forms';

import {getChoices} from 'utils/choices';
import _ from 'utils/i18n';
import {CancelButton} from 'components/buttons';

import RecipientField from './RecipientField';
import ZoteroKeysField from './ZoteroKeysField';


const NameLabel = _('Name');
const DescriptionLabel = _('Description');
const IntervalLabel = _('Interval');

const Intervals = getChoices('interval');

const DefaultValues = {
    interval: Intervals[0].value,
};

const getDefaultValues = data => {
    if (!data) return DefaultValues;

    return {
        ...data,
        recipients: data.recipients.join('\n'),
        zotero_keys: data.zotero_keys.join('\n'),
    };
};

const MonitorForm = ({endpoint, method, backURL, successMessage, data, submitLabel, ...props}) => {
    const getRedirectURL = ({id}) => `/monitor/${id}/`;
    const [onSubmit, {control, register, errors}] = useMutationForm(
        endpoint,
        {defaultValues: getDefaultValues(data)},
        {
            method,
            successMessage,
            redirectURL: getRedirectURL,
        },
    );

    return (
        <form className="my-4 w-full max-w-screen-md" onSubmit={onSubmit} {...props}>
            <TextInput
                register={register({required: true})}
                name="name"
                label={NameLabel}
                errors={errors}
                required
            />
            <TextArea
                register={register({required: false})}
                name="description"
                label={DescriptionLabel}
                errors={errors}
                fill
                growVertically
                rows="5"
            />
            <Select
                control={control}
                name="interval"
                label={IntervalLabel}
                errors={errors}
                choices={Intervals}
                required
            />
            <RecipientField register={register} errors={errors} />
            <ZoteroKeysField register={register} errors={errors} />
            <div className="flex justify-between">
                <CancelButton to={backURL} />

                <Button type="submit" intent={Intent.PRIMARY} text={submitLabel} />
            </div>
        </form>
    );
};

export default MonitorForm;
