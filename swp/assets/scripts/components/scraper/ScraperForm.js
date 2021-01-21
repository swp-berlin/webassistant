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
    DocumentResolverForm,
    LinkResolverForm,
    ListResolverForm,
    FieldResolverForm,
    TagResolverForm,
    TagDataResolverForm,
    TagAttributeResolverForm,
    TagStaticResolverForm,
} from './ResolverForm/forms';

import ScraperTypeSelect from './ScraperTypeSelect';
import ScraperFormErrors from './ScraperFormErrors';
import ScraperTypeDescription from './ScraperTypeDescription';


const StartURLLabel = _('Start-URL');
const EnabledLabel = _('Enabled');
const TypeLabel = _('Scraper Type');
const IntervalLabel = _('Interval');
const ConfigLabel = _('Config');
const SubmitButtonLabel = _('Save');

const Intervals = getChoices('interval');

const Forms = {
    List: ListResolverForm,
    Link: LinkResolverForm,
    Data: FieldResolverForm,
    Attribute: FieldResolverForm,
    Static: FieldResolverForm,
    Document: DocumentResolverForm,
    Tag: TagResolverForm,
    TagData: TagDataResolverForm,
    TagAttribute: TagAttributeResolverForm,
    TagStatic: TagStaticResolverForm,
};

const DEFAULT_VALUES = {
    is_active: false,
    interval: Intervals[0].value,
    type: ScraperTypes[0].value,
    data: ScraperTypes[0].defaults,
};

const ScraperForm = ({endpoint, data, method, redirectURL}) => {
    const [onSubmit, form] = useMutationForm(
        endpoint,
        {defaultValues: data || DEFAULT_VALUES},
        {method, redirectURL},
    );
    const {control, register, errors} = form;

    return (
        <div className="flex space-x-8 my-4">
            <form className="scraper-form w-3/6" onSubmit={onSubmit}>
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
                    required
                />

                <Field label={ConfigLabel}>
                    <ResolverFormProvider value={Forms}>
                        <ResolverForm form={form} prefix="data" />
                    </ResolverFormProvider>
                </Field>

                <ScraperFormErrors form={form} errors={errors} />

                <Button type="submit" intent="primary" text={SubmitButtonLabel} />
            </form>
            <ScraperTypeDescription form={form} />
        </div>
    );
};

ScraperForm.defaultProps = {
    method: 'POST',
};

export default ScraperForm;
