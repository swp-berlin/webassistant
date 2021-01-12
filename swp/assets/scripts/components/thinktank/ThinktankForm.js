import {useMutationForm} from 'components/Fetch';
import {TextArea, TextInput} from 'components/forms';
import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {CancelButton} from 'components/buttons';


const NameLabel = _('Name');
const DescriptionLabel = _('Description');
const URLLabel = _('URL');
const UniqueFieldLabel = _('Unique Field');
const SaveLabel = _('Save');
const CreateLabel = _('Create');

const CreatedMessage = _('Successfully created thinktank');
const ChangedMessage = _('Successfully changed thinktank');

const ThinktankForm = ({endpoint, method, redirectURL, successMessage, data, submitLabel, ...props}) => {
    const [onSubmit, {register, errors}] = useMutationForm(
        endpoint,
        {defaultValues: data},
        {
            method,
            successMessage,
            redirectURL,
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
            <TextInput
                register={register({required: true})}
                name="url"
                type="url"
                label={URLLabel}
                errors={errors}
                required
            />
            <TextInput
                register={register({required: true})}
                name="unique_field"
                label={UniqueFieldLabel}
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

            <div className="flex justify-between">
                <CancelButton to={redirectURL} />

                <Button type="submit" intent={Intent.PRIMARY} text={submitLabel} />
            </div>
        </form>
    );
};

export const ThinktankAddForm = ({endpoint, ...props}) => (
    <ThinktankForm endpoint={endpoint || '/thinktank/'} {...props} />
);

ThinktankAddForm.defaultProps = {
    method: 'POST',
    submitLabel: CreateLabel,
    successMessage: CreatedMessage,
};

export const ThinktankEditForm = ({endpoint, data, ...props}) => (
    <ThinktankForm endpoint={endpoint || `/thinktank/${data.id}/`} data={data} {...props} />
);

ThinktankEditForm.defaultProps = {
    method: 'PUT',
    submitLabel: SaveLabel,
    successMessage: ChangedMessage,
};

export default ThinktankForm;
