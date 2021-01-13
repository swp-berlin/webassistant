import {Button, Intent} from '@blueprintjs/core';
import {useMutationForm} from 'components/Fetch';
import {TextArea, TextInput} from 'components/forms';

import _ from 'utils/i18n';
import {CancelButton} from 'components/buttons';


const NameLabel = _('Name');
const DescriptionLabel = _('Description');
const URLLabel = _('URL');
const UniqueFieldLabel = _('Unique Field');


const ThinktankForm = ({endpoint, method, backURL, successMessage, data, submitLabel, ...props}) => {
    const getRedirectURL = ({id}) => `/thinktank/${id}/`;
    const [onSubmit, {register, errors}] = useMutationForm(
        endpoint,
        {defaultValues: data},
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
                <CancelButton to={backURL} />

                <Button type="submit" intent={Intent.PRIMARY} text={submitLabel} />
            </div>
        </form>
    );
};

export default ThinktankForm;
