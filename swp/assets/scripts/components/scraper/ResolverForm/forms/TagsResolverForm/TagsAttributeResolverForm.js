import _ from 'utils/i18n';

import {TextInput} from 'components/forms';
import TagsDataResolverForm from './TagsDataResolverForm';


const AttributeLabel = _('Attribute');

const TagsAttributeResolverForm = props => {
    const {form: {register, errors}, prefix, field} = props;

    return (
        <TagsDataResolverForm {...props}>
            <TextInput
                register={register()}
                name={`${prefix}.attribute`}
                label={AttributeLabel}
                errors={errors}
                defaultValue={field.attribute}
            />
        </TagsDataResolverForm>
    );
};

export default TagsAttributeResolverForm;
