import {useMutationForm} from 'components/Fetch';
import {TextArea, TextInput} from 'components/forms';
import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {BackButton} from 'components/buttons';


const NameLabel = _('Name');
const DescriptionLabel = _('Description');
const URLLabel = _('URL');
const UniqueFieldLabel = _('Unique Field');
const SaveLabel = _('Save');
const CreateLabel = _('Create');

const ThinktankForm = ({endpoint, method, redirectURL, successMessage, data, submitLabel, ...props}) => {
    const id = data ? data.id : undefined;

    const defaultEndpoint = id ? '/thinktank/' : `/thinktank/${id}`;
    const defaultMethod = id ? 'PUT' : 'POST';
    const defaultSubmitLabel = id ? SaveLabel : CreateLabel;

    const [onSubmit, {register, errors}] = useMutationForm(
        endpoint || defaultEndpoint,
        {defaultValues: data},
        {
            method: method || defaultMethod,
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
                <BackButton to={redirectURL} />
                <Button type="submit" intent={Intent.PRIMARY} text={submitLabel || defaultSubmitLabel} />
            </div>
        </form>
    );
};

export default ThinktankForm;
