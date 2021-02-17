import Select from 'components/forms/Select/Select';
import {ChoicesQuery} from 'components/Fetch';

import _ from 'utils/i18n';


const ThinktankLabel = _('Thinktank');

const ThinktankSelect = ({form: {control, errors}}) => (
    <ChoicesQuery
        endpoint="/thinktank/"
        params={{is_active: true}}
    >
        <Select
            control={control}
            name="thinktank"
            label={ThinktankLabel}
            errors={errors}
        />
    </ChoicesQuery>
);


export default ThinktankSelect;
