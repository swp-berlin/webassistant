import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';

import {Select} from 'components/forms';

const Name = 'interval';
const Label = _('Interval');
const Choices = getChoices('interval');
const {value: DefaultValue} = Choices.at(0);

export const DefaultValues = {
    [Name]: [DefaultValue],
};

const IntervalSelect = ({control, errors}) => (
    <Select
        control={control}
        name={Name}
        label={Label}
        errors={errors}
        choices={Choices}
        required
    />
);

export default IntervalSelect;
