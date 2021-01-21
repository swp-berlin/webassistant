import _ from 'utils/i18n';

import {Select} from 'components/forms';


import TagDataResolverForm from './TagDataResolverForm';
import TagAttributeResolverForm from './TagAttributeResolverForm';
import TagStaticResolverForm from './TagStaticResolverForm';


const TagLabel = _('Tag');
const TypeLabel = _('Type');

const TagResolverChoices = [
    {value: 'TagData', label: 'Data'},
    {value: 'TagAttribute', label: 'Attribute'},
    {value: 'TagStatic', label: 'Static'},
];

const TagForms = {
    TagData: TagDataResolverForm,
    TagAttribute: TagAttributeResolverForm,
    TagStatic: TagStaticResolverForm,
};

const TagResolverForm = props => {
    const {form: {register, control, watch}, prefix, field} = props;

    const type = watch(`${prefix}.resolver.type`, 'TagData');
    const Form = TagForms[type];

    return (
        <div>
            <h2 className="text-lg mb-4">{TagLabel}</h2>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="Tag" />
            <Select
                control={control}
                name={`${prefix}.resolver.type`}
                label={TypeLabel}
                choices={TagResolverChoices}
                defaultValue="TagData"
            />
            <Form {...props} prefix={`${prefix}.resolver`} field={field.resolver} />
        </div>
    );
};

export default TagResolverForm;
