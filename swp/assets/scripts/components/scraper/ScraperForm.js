import {useMutationForm} from 'components/Fetch';
import {Select, TextArea, TextInput} from 'components/forms';
import {Button, Checkbox} from '@blueprintjs/core';

import {getChoices} from 'utils/choices';
import _ from 'utils/i18n';

const StartURLLabel = _('Start-URL');
const EnabledLabel = _('Enabled');
const TypeLabel = _('Scraper Type');
const IntervalLabel = _('Interval');
const ConfigLabel = _('Config');
const SubmitButtonLabel = _('Save');

const Intervals = getChoices('interval');
const ScraperTypes = getChoices('ScraperType');

const ScraperForm = ({id, data}) => {
    const [onSubmit, {control, register, errors}] = useMutationForm(
        `/scraper/${id}/`,
        {
            defaultValues: {
                ...data,
                data: JSON.stringify(data.data, null, 2),
            },
        },
        {method: 'PATCH'},
    );

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
            <TextArea
                register={register({required: true})}
                name="data"
                label={ConfigLabel}
                errors={errors}
                growVertically
                fill
            />
            <Button type="submit" intent="primary" text={SubmitButtonLabel} />
        </form>
    );
};

export default ScraperForm;
