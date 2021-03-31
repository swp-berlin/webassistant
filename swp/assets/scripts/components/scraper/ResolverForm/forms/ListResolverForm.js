import _ from 'utils/i18n';
import {getChoices} from 'utils/choices';
import {NumericInput} from 'components/forms';
import {Select} from 'components/forms/Select';

import ResolverListForm from '../ResolverListForm';
import SelectorField from './SelectorField';


const ListLabel = _('List');
const ListSelectorLabel = _('List Selector');
const ItemSelectorLabel = _('Item Selector');
const PaginatorTypeLabel = _('Paginator Type');
const PaginationButtonSelectorLabel = _('Pagination Button Selector');
const MaxPagesLabel = _('Max Pages');

const PaginatorTypes = getChoices('PaginatorType');


const ListResolverForm = ({form, prefix, level, readOnly}) => {
    const {control, register, errors} = form;

    return (
        <ResolverListForm form={form} prefix={prefix} level={level} readOnly={readOnly}>
            <h2 className="text-lg mb-4">{ListLabel}</h2>
            <input name={`${prefix}.type`} ref={register({required: true})} type="hidden" defaultValue="List" />
            <SelectorField
                register={register}
                name={`${prefix}.paginator.list_selector`}
                label={ListSelectorLabel}
                errors={errors}
                required
                readOnly={readOnly}
            />
            <SelectorField
                register={register}
                name={`${prefix}.selector`}
                label={ItemSelectorLabel}
                errors={errors}
                required
                readOnly={readOnly}
            />
            <Select
                name={`${prefix}.paginator.type`}
                label={PaginatorTypeLabel}
                control={control}
                choices={PaginatorTypes}
                errors={errors}
                disabled={readOnly}
                defaultValue={PaginatorTypes[0].value}
            />
            <SelectorField
                register={register}
                name={`${prefix}.paginator.button_selector`}
                label={PaginationButtonSelectorLabel}
                errors={errors}
                readOnly={readOnly}
            />
            <NumericInput
                control={control}
                name={`${prefix}.paginator.max_pages`}
                label={MaxPagesLabel}
                errors={errors}
                defaultValue="1"
                min={1}
                fill
                readOnly={readOnly}
            />
        </ResolverListForm>
    );
};

export default ListResolverForm;
