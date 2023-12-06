import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';

import {CancelButton} from 'components/buttons';
import {ChoicesQuery, useMutationForm} from 'components/Fetch';
import {MultiSelect, Select, TextArea, TextInput} from 'components/forms';

const PoolLabel = _('Pool');
const NameLabel = _('Name');
const DescriptionLabel = _('Description');
const URLLabel = _('URL');
const UniqueFieldLabel = _('Unique Field');

const UniqueChoices = getChoices('UniqueKey');

export const DefaultValues = {
    unique_fields: [UniqueChoices[0].value],
};

const getRedirectURL = ({id}) => `/thinktank/${id}/`;

const PoolQueryParams = {can_manage: true};

const preparePoolChoice = ({id, name}) => ({value: id, label: name});

const ThinktankForm = ({endpoint, method, backURL, successMessage, data, submitLabel, ...props}) => {
    const [onSubmit, {control, register, errors}] = useMutationForm(
        endpoint,
        {defaultValues: data || DefaultValues},
        {
            method,
            successMessage,
            redirectURL: getRedirectURL,
        },
    );

    return (
        <form className="my-4 w-full max-w-screen-md" onSubmit={onSubmit} {...props}>
            <ChoicesQuery endpoint="pool" params={PoolQueryParams} prepareChoice={preparePoolChoice}>
                <Select name="pool" label={PoolLabel} control={control} errors={errors} required />
            </ChoicesQuery>
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
            <MultiSelect
                name="unique_fields"
                label={UniqueFieldLabel}
                choices={UniqueChoices}
                control={control}
                errors={errors}
                required
                fill
            />
            <TextArea
                register={register({required: false})}
                name="description"
                label={DescriptionLabel}
                errors={errors}
                fill
                growVertically
                rows={5}
            />
            <div className="flex justify-between">
                <CancelButton to={backURL} />
                <Button type="submit" intent={Intent.PRIMARY} text={submitLabel} />
            </div>
        </form>
    );
};

export default ThinktankForm;
