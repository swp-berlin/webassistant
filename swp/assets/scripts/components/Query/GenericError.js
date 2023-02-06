import {faSadTear} from '@fortawesome/free-solid-svg-icons/faSadTear';

import _ from 'utils/i18n';
import {getErrorMessage} from 'utils/react-query-fetch';

import BaseError from 'components/Fetch/BaseError';

const Title = _('Error');

const GenericError = ({error}) => (
    <BaseError
        status={null}
        Fallback={{
            icon: faSadTear,
            title: Title,
            description: getErrorMessage(error),
        }}
    />
);

export default GenericError;
