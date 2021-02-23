import {useCallback, useState} from 'react';
import {useMutationForm} from 'components/Fetch';
import {Select, TextInput} from 'components/forms';
import {Button} from '@blueprintjs/core';

import ScraperTypes from 'schemes/scraperTypes.json';
import {getChoices} from 'utils/choices';
import _ from 'utils/i18n';
import Field from 'components/forms/Field';
import Portal from 'components/Portal';

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
    AuthorsResolverForm,
} from './ResolverForm/forms';
import {Preview, PreviewButton} from './preview';

import ScraperTypeSelect from './ScraperTypeSelect';
import ScraperFormErrors from './ScraperFormErrors';
import ScraperTypeDescription from './ScraperTypeDescription';
import ScraperActivationButton from './ScraperActivationButton';


const StartURLLabel = _('Start URL');
const TypeLabel = _('Scraper Type');
const IntervalLabel = _('Interval');
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
    Tag: TagResolverForm,
    TagData: TagDataResolverForm,
    TagAttribute: TagAttributeResolverForm,
    TagStatic: TagStaticResolverForm,
    Authors: AuthorsResolverForm,
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

    // eslint-disable-next-line no-unused-vars
    const [onSubmit, form, result, mutate] = useMutationForm(
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

    return (
        <form className="mt-8 scraper-form grid grid-cols-1 lg:grid-cols-2 gap-8" onSubmit={handleSubmit}>
            {id && (
                <Portal id="scraper-activation-container">
                    <ScraperActivationButton id={id} isActive={isActive} form={form} onToggle={setIsActive} />
                </Portal>
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

                <ScraperFormErrors form={form} errors={errors} />

                <div className="flex justify-end space-x-2">
                    <Button type="submit" intent="primary" text={SubmitButtonLabel} disabled={isActive} />
                </div>
            </div>

            <div>
                {preview && <Preview id={preview} />}
            </div>
        </form>
    );
};

ScraperForm.defaultProps = {
    method: 'POST',
};

export default ScraperForm;
