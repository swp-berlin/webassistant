import {Button, Intent} from '@blueprintjs/core';
import {useMutationForm} from 'components/Fetch';

import {CancelButton} from 'components/buttons';
import ThinktankSelect from './ThinktankSelect';
import PublicationFiltersForm from './PublicationFiltersForm';


const DefaultValues = {
    filters: [],
};

const ThinktankFilterForm = ({endpoint, method, backURL, successMessage, data, submitLabel, redirectURL, ...props}) => {
    const [onSubmit, form] = useMutationForm(
        endpoint,
        {defaultValues: data || DefaultValues},
        {method, successMessage, redirectURL},
    );

    return (
        <form className="my-4 w-full max-w-screen-md" onSubmit={onSubmit} {...props}>
            <ThinktankSelect form={form} />

            <PublicationFiltersForm form={form} />

            <div className="flex justify-between">
                <CancelButton to={backURL} />

                <Button type="submit" intent={Intent.PRIMARY} text={submitLabel} />
            </div>
        </form>
    );
};

export default ThinktankFilterForm;
