import _ from 'utils/i18n';

import {Select} from 'components/forms';
import {getChoices} from 'utils/choices';

import TagDataResolverForm from './TagDataResolverForm';
import TagAttributeResolverForm from './TagAttributeResolverForm';
import TagStaticResolverForm from './TagStaticResolverForm';


const TagLabel = _('Tag');
const TypeLabel = _('Type');

const TagResolverChoices = getChoices('TagResolverType');

const TagForms = {
    TagData: TagDataResolverForm,
    TagAttribute: TagAttributeResolverForm,
    TagStatic: TagStaticResolverForm,
};

const TagResolverForm = props => {
    const {form: {register, control, watch}, prefix, field, readOnly} = props;

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
                disabled={readOnly}
            />
            <Form {...props} prefix={`${prefix}.resolver`} field={field.resolver || {}} readOnly={readOnly} />
        </div>
    );
};

export default TagResolverForm;
