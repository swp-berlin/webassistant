import {useCallback, useState} from 'react';
import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';

import {useMutationForm} from 'components/Fetch';
import {Select, TextInput} from 'components/forms';
import Field from 'components/forms/Field';

import ScraperTypes from 'schemes/scraperTypes.json';

import ResolverForm from './ResolverForm/ResolverForm';
import ResolverFormProvider from './ResolverForm/ResolverFormContext';
import {
    DocumentResolverForm,
    LinkResolverForm,
    ListResolverForm,
    FieldResolverForm,
} from './ResolverForm/forms';
import {Preview, PreviewButton} from './preview';
import BackendScraperErrors from './BackendScraperErrors';
import CategorySelect from './CategorySelect';
import ScraperTypeSelect from './ScraperTypeSelect';
import ScraperFormErrors from './ScraperFormErrors';
import ScraperTypeDescription from './ScraperTypeDescription';
import ScraperActivationButton from './ScraperActivationButton';
import {ScraperActivationPortal} from './ScraperActivationContainer';

const StartURLLabel = _('Start URL');
const TypeLabel = _('Scraper Type');
const IntervalLabel = _('Interval');
const CategoriesLabel = _('Categories');
const ConfigLabel = _('Config');
const SubmitButtonLabel = _('Save');
const DisabledTitle = _('You have to deactivate the scraper in order to edit it.');

const Intervals = getChoices('interval');

const Forms = {
    List: ListResolverForm,
    Link: LinkResolverForm,
    Data: FieldResolverForm,
    Attribute: FieldResolverForm,
    Static: FieldResolverForm,

    Document: DocumentResolverForm,

    Title: FieldResolverForm,
    Subtitle: FieldResolverForm,
    Abstract: FieldResolverForm,
    Publication_Date: FieldResolverForm,
    URL: FieldResolverForm,
    Authors: FieldResolverForm,
    DOI: FieldResolverForm,
    ISBN: FieldResolverForm,
    Tags: FieldResolverForm,
};

const DEFAULT_VALUES = {
    interval: Intervals[0].value,
    type: ScraperTypes[0].value,
    data: ScraperTypes[0].defaults,
};

const ScraperForm = ({endpoint, data, method, redirectURL}) => {
    const id = data?.id;

    const [preview, setPreview] = useState(null);
    const handlePreview = useCallback(preview => setPreview(preview.id), []);

    const [, form, , mutate] = useMutationForm(
        endpoint,
        {defaultValues: data || DEFAULT_VALUES},
        {method, redirectURL},
    );
    const {control, register, errors} = form;

    const [isActive, setIsActive] = useState(!!data?.is_active);

    const handleSubmit = useCallback(async event => {
        event.preventDefault();
        form.clearErrors();
        const valid = await form.trigger('start_url');

        if (valid) await mutate(form.getValues(), id ? 'PATCH' : 'POST');
    }, [form, id, mutate]);

    const disabledTitle = isActive ? DisabledTitle : null;
    const scraperErrors = data?.errors;

    return (
        <form className="mt-8 scraper-form grid grid-cols-1 lg:grid-cols-2 gap-8" onSubmit={handleSubmit}>
            {id && (
                <ScraperActivationPortal>
                    <ScraperActivationButton id={id} isActive={isActive} form={form} onToggle={setIsActive} />
                </ScraperActivationPortal>
            )}
            <div>
                <TextInput
                    register={register({required: true})}
                    name="start_url"
                    label={StartURLLabel}
                    errors={errors}
                    readOnly={isActive}
                    title={disabledTitle}
                />
                <ScraperTypeSelect
                    form={form}
                    name="type"
                    label={TypeLabel}
                    errors={errors}
                    choices={ScraperTypes}
                    disabled={isActive}
                    title={disabledTitle}
                />
                <Select
                    control={control}
                    name="interval"
                    label={IntervalLabel}
                    errors={errors}
                    choices={Intervals}
                    required
                    disabled={isActive}
                    title={disabledTitle}
                />
                <CategorySelect
                    control={control}
                    name="categories"
                    label={CategoriesLabel}
                    errors={errors}
                    disabled={isActive}
                    title={disabledTitle}
                    fill
                />
            </div>

            <div>
                <ScraperTypeDescription form={form} />
                <PreviewButton form={form} onPreview={handlePreview} />
            </div>

            <div>
                <Field label={ConfigLabel}>
                    <ResolverFormProvider value={Forms}>
                        <ResolverForm form={form} prefix="data" readOnly={isActive} />
                    </ResolverFormProvider>
                </Field>

                <ScraperFormErrors form={form} />

                <div className="flex justify-end space-x-2">
                    <Button type="submit" intent="primary" text={SubmitButtonLabel} disabled={isActive} />
                </div>
            </div>

            <div>
                {preview ? <Preview id={preview} /> : <BackendScraperErrors errors={scraperErrors} />}
            </div>
        </form>
    );
};

ScraperForm.defaultProps = {
    method: 'POST',
};

export default ScraperForm;
