import {useMutationForm} from 'components/Fetch';
import {Select, TextInput} from 'components/forms';
import {Button, Checkbox} from '@blueprintjs/core';


import {getChoices} from 'utils/choices';
import _ from 'utils/i18n';
import Field from 'components/forms/Field';

import ResolverForm from './ResolverForm/ResolverForm';
import ResolverFormProvider from './ResolverForm/ResolverFormContext';
import {
    AttributeResolverForm,
    DataResolverForm,
    DocumentResolverForm,
    LinkResolverForm,
    ListResolverForm,
    StaticResolverForm,
} from './ResolverForm/forms';


const StartURLLabel = _('Start-URL');
const EnabledLabel = _('Enabled');
const TypeLabel = _('Scraper Type');
const IntervalLabel = _('Interval');
const ConfigLabel = _('Config');
const SubmitButtonLabel = _('Save');

const Intervals = getChoices('interval');
const ScraperTypes = getChoices('ScraperType');

const Forms = {
    List: ListResolverForm,
    Data: DataResolverForm,
    Link: LinkResolverForm,
    Attribute: AttributeResolverForm,
    Document: DocumentResolverForm,
    Static: StaticResolverForm,
};

const ScraperForm = ({id, data}) => {
    const [onSubmit, form] = useMutationForm(
        `/scraper/${id}/`,
        {
            defaultValues: data,
        },
        {method: 'PATCH'},
    );

    const {control, register, errors} = form;

    return (
        <form className="my-4 w-full max-w-screen-md" onSubmit={onSubmit}>
            <TextInput
                register={register({required: true})}
                name="start_url"
                label={StartURLLabel}
                errors={errors}
            />
            <Checkbox
                name="is_active"
                inputRef={register}
                inline
                label={EnabledLabel}
            />
            <Select
                control={control}
                name="type"
                label={TypeLabel}
                errors={errors}
                choices={ScraperTypes}
            />
            <Select
                control={control}
                name="interval"
                label={IntervalLabel}
                errors={errors}
                choices={Intervals}
            />

            <Field label={ConfigLabel}>
                <ResolverFormProvider value={Forms}>
                    <ResolverForm form={form} prefix="data" />
                </ResolverFormProvider>
            </Field>

            <Button type="submit" intent="primary" text={SubmitButtonLabel} />
        </form>
    );
};

export default ScraperForm;
