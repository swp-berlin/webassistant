import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {useMutationForm} from 'components/Fetch';
import {CancelButton} from 'components/buttons';
import {Select, TextArea, TextInput} from 'components/forms';
import PoolChoicesQuery from 'components/PoolChoicesQuery';
import {useRegister} from 'components/thinktank/Register';

import IntervalSelect, {DefaultValues} from './IntervalSelect';
import RecipientField from './RecipientField';
import ZoteroKeysField from './ZoteroKeysField';

const PoolLabel = _('Pool');
const NameLabel = _('Name');
const DescriptionLabel = _('Description');

export {DefaultValues};

const getDefaultValues = data => {
    if (!data) return DefaultValues;

    return {
        ...data,
        pool: data.pool.id,
        recipients: data.recipients.join('\n'),
        zotero_keys: data.zotero_keys.join('\n'),
    };
};

const getRedirectURL = ({id}) => `/monitor/${id}/`;

const MonitorForm = ({endpoint, method, backURL, successMessage, data, defaultValues, submitLabel, ...props}) => {
    const formOptions = {defaultValues: defaultValues || getDefaultValues(data)};
    const mutationOptions = {method, successMessage, redirectURL: getRedirectURL};
    const [onSubmit, form] = useMutationForm(endpoint, formOptions, mutationOptions, [successMessage]);
    const {control, register, errors} = form;
    const Register = useRegister(register, errors);

    return (
        <form className="my-4 w-full max-w-screen-md" onSubmit={onSubmit} {...props}>
            <PoolChoicesQuery canManage>
                <Select name="pool" label={PoolLabel} control={control} errors={errors} required />
            </PoolChoicesQuery>
            <Register required>
                <TextInput name="name" label={NameLabel} />
            </Register>
            <Register>
                <TextArea name="description" label={DescriptionLabel} rows={5} growVertically fill />
            </Register>
            <IntervalSelect control={control} errors={errors} />
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
