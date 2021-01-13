import ResolverListForm from '../../ResolverListForm';


const TagsResolverChoices = [
    {value: 'TagsData', label: 'Data'},
    {value: 'TagsAttribute', label: 'Attribute'},
    {value: 'TagsStatic', label: 'Static'},
];

const TagsResolverForm = ({form, prefix, level}) => (
    <ResolverListForm form={form} prefix={prefix} level={level} choices={TagsResolverChoices} />
);

export default TagsResolverForm;
