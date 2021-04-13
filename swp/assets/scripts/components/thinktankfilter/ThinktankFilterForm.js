import {useCallback, useState} from 'react';
import {Button, Intent} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {useMutationForm} from 'components/Fetch';
import {CancelButton} from 'components/buttons';
import PublicationList from 'components/publication/PublicationList';

import ThinktankSelect from './ThinktankSelect';
import PublicationFiltersForm from './PublicationFiltersForm';
import PreviewButton from './PreviewButton';


const PreviewHeading = _('Preview');

const DefaultValues = {
    filters: [],
};

const ThinktankFilterForm = ({endpoint, method, backURL, successMessage, data, submitLabel, redirectURL, ...props}) => {
    const [onSubmit, form] = useMutationForm(
        endpoint,
        {defaultValues: data || DefaultValues},
        {method, successMessage, redirectURL},
    );

    const [preview, setPreview] = useState(null);
    const handlePreview = useCallback(publications => setPreview(publications), []);

    return (
        <form className="my-4 w-full max-w-screen-md" onSubmit={onSubmit} {...props}>
            <ThinktankSelect form={form} />

            <PublicationFiltersForm form={form} />

            <div className="flex justify-between">
                <CancelButton to={backURL} />

                <div className="flex space-x-2">
                    <PreviewButton form={form} onPreview={handlePreview} />
                    <Button type="submit" intent={Intent.PRIMARY} text={submitLabel} />
                </div>
            </div>

            <div>
                {preview && (
                    <div className="mt-8">
                        <h4>{PreviewHeading}</h4>
                        <PublicationList items={preview} className="mt-4" />
                    </div>
                )}
            </div>
        </form>
    );
};

export default ThinktankFilterForm;
