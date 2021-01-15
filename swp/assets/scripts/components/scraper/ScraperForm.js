import {useMutationForm} from 'components/Fetch';
import {Checkbox, Select, TextInput} from 'components/forms';
import {Button} from '@blueprintjs/core';

import ScraperTypes from 'schemes/scraperTypes.json';
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
    TagsResolverForm,
    TagsDataResolverForm,
    TagsAttributeResolverForm,
    TagsStaticResolverForm,
} from './ResolverForm/forms';

import ScraperTypeSelect from './ScraperTypeSelect';
import ScraperFormErrors from './ScraperFormErrors';


const StartURLLabel = _('Start-URL');
const EnabledLabel = _('Enabled');
const TypeLabel = _('Scraper Type');
const IntervalLabel = _('Interval');
const ConfigLabel = _('Config');
const SubmitButtonLabel = _('Save');

const Intervals = getChoices('interval');

const Forms = {
    List: ListResolverForm,
    Data: DataResolverForm,
    Link: LinkResolverForm,
    Attribute: AttributeResolverForm,
    Document: DocumentResolverForm,
    Static: StaticResolverForm,
    Tags: TagsResolverForm,
    TagsData: TagsDataResolverForm,
    TagsAttribute: TagsAttributeResolverForm,
    TagsStatic: TagsStaticResolverForm,
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
        <form className="scraper-form my-4 w-full max-w-screen-md" onSubmit={onSubmit}>
            <TextInput
                register={register({required: true})}
                name="start_url"
                label={StartURLLabel}
                errors={errors}
            />
            <Checkbox
                name="is_active"
                control={control}
                inline
                label={EnabledLabel}
            />
            <ScraperTypeSelect
                form={form}
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

            <ScraperFormErrors form={form} errors={errors} />

            <Button type="submit" intent="primary" text={SubmitButtonLabel} />
        </form>
    );
};

export default ScraperForm;
