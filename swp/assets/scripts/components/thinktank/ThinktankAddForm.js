import {useMemo} from 'react';
import {useLocation} from 'react-router-dom';

import _ from 'utils/i18n';

import ThinktankForm, {DefaultValues} from './ThinktankForm';

const SubmitLabel = _('Create');
const SuccessMessage = _('Successfully created thinktank');

export const useDefaultValues = defaultValues => {
    const {search} = useLocation();

    return useMemo(
        () => {
            if (search) {
                const params = new URLSearchParams(search);

                let pool = params.get('pool');

                if (pool) {
                    pool = parseInt(pool);

                    return Number.isNaN(pool) ? defaultValues : {...defaultValues, pool};
                }
            }

            return defaultValues;
        },
        [search, defaultValues],
    );
};

const ThinktankAddForm = ({endpoint, ...props}) => {
    const data = useDefaultValues(DefaultValues);

    return <ThinktankForm endpoint={endpoint || '/thinktank/'} data={data} {...props} />;
};

ThinktankAddForm.defaultProps = {
    method: 'POST',
    submitLabel: SubmitLabel,
    successMessage: SuccessMessage,
};

export default ThinktankAddForm;
