import _ from 'utils/i18n';
import ThinktankForm from './ThinktankForm';


const SubmitLabel = _('Save');
const SuccessMessage = _('Successfully changed thinktank');

const ThinktankEditForm = ({endpoint, data, ...props}) => (
    <ThinktankForm endpoint={endpoint || `/thinktank/${data.id}`} data={data} {...props} />
);

ThinktankEditForm.defaultProps = {
    method: 'PUT',
    submitLabel: SubmitLabel,
    successMessage: SuccessMessage,
};

export default ThinktankEditForm;
