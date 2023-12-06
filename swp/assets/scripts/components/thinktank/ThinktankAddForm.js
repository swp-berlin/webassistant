import {useMemo} from 'react';
import {useLocation} from 'react-router-dom';

import _ from 'utils/i18n';

import ThinktankForm, {DefaultValues} from './ThinktankForm';

const SubmitLabel = _('Create');
const SuccessMessage = _('Successfully created thinktank');

const useDefaultValues = () => {
    const {search} = useLocation();

    return useMemo(
        () => {
            if (search) {
                const params = new URLSearchParams(search);
                const pool = params.get('pool');

                if (pool) return {...DefaultValues, pool: +pool};
            }

            return DefaultValues;
        },
        [search],
    );
};

const ThinktankAddForm = ({endpoint, ...props}) => {
    const data = useDefaultValues();

    return <ThinktankForm endpoint={endpoint || '/thinktank/'} data={data} {...props} />;
};

ThinktankAddForm.defaultProps = {
    method: 'POST',
    submitLabel: SubmitLabel,
    successMessage: SuccessMessage,
};

export default ThinktankAddForm;
