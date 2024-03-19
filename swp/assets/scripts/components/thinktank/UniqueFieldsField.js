import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';

import {MultiSelect} from 'components/forms';

const Name = 'unique_fields';
const Label = _('Unique Field');
const Choices = getChoices('UniqueKey');
const {value: DefaultValue} = Choices.at(0);

export const DefaultValues = {
    [Name]: [DefaultValue],
};

const UniqueFieldsField = ({control, errors}) => (
    <MultiSelect
        name={Name}
        label={Label}
        choices={Choices}
        control={control}
        errors={errors}
        required
        fill
    />
);

export default UniqueFieldsField;
