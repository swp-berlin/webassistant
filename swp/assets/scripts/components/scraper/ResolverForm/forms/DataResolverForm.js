import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';
import {Select} from 'components/forms/Select';

import SelectorField from './SelectorField';


const KeyLabel = _('Field');
const SelectorLabel = _('Selector');

const KeyChoices = getChoices('DataResolverKey');

const DataResolverForm = props => {
    const {form, prefix, field, children, readOnly} = props;
    const {register, errors} = form;

    return (
        <>
            <Select
                control={form.control}
                name={`${prefix}.key`}
                label={KeyLabel}
                choices={KeyChoices}
                errors={errors}
                defaultValue={field.key || KeyChoices[0].value}
                disabled={readOnly}
            />
            <SelectorField
                register={register}
                name={`${prefix}.selector`}
                label={SelectorLabel}
                errors={errors}
                defaultValue={field.selector}
                required
                readOnly={readOnly}
            />
            {children}
        </>
    );
};

export default DataResolverForm;
