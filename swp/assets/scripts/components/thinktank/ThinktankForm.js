import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {CancelButton} from 'components/buttons';
import {useMutationForm} from 'components/Fetch';
import {Select, TextArea, TextInput} from 'components/forms';
import PoolChoicesQuery from 'components/PoolChoicesQuery';

import {useRegister} from './Register';
import UniqueFieldsField, {DefaultValues} from './UniqueFieldsField';

const PoolLabel = _('Pool');
const DomainLabel = _('Domain');
const NameLabel = _('Name');
const DescriptionLabel = _('Description');
const URLLabel = _('URL');

export {DefaultValues};

const getRedirectURL = ({id}) => `/thinktank/${id}/`;

const ThinktankForm = ({endpoint, method, backURL, successMessage, data, submitLabel, ...props}) => {
    const formOptions = {defaultValues: data || DefaultValues};
    const mutationOptions = {method, successMessage, redirectURL: getRedirectURL};
    const [onSubmit, {control, register, errors}] = useMutationForm(endpoint, formOptions, mutationOptions);
    const Register = useRegister(register, errors);

    return (
        <form className="my-4 w-full max-w-screen-md" onSubmit={onSubmit} {...props}>
            <PoolChoicesQuery canManage>
                <Select name="pool" label={PoolLabel} control={control} errors={errors} required />
            </PoolChoicesQuery>
            <Register required>
                <TextInput name="domain" label={DomainLabel} />
            </Register>
            <Register required>
                <TextInput name="name" label={NameLabel} />
            </Register>
            <Register required>
                <TextInput name="url" type="url" label={URLLabel} />
            </Register>
            <UniqueFieldsField control={control} errors={errors} />
            <Register>
                <TextArea name="description" label={DescriptionLabel} rows={5} growVertically fill />
            </Register>
            <div className="flex justify-between">
                <CancelButton to={backURL} />
                <Button type="submit" intent={Intent.PRIMARY} text={submitLabel} />
            </div>
        </form>
    );
};

export default ThinktankForm;
