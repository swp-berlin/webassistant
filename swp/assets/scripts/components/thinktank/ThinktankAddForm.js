import _ from 'utils/i18n';
import ThinktankForm from './ThinktankForm';


const SubmitLabel = _('Create');
const SuccessMessage = _('Successfully created thinktank');

const ThinktankAddForm = ({endpoint, ...props}) => (
    <ThinktankForm endpoint={endpoint || '/thinktank/'} {...props} />
);

ThinktankAddForm.defaultProps = {
    method: 'POST',
    submitLabel: SubmitLabel,
    successMessage: SuccessMessage,
};

export default ThinktankAddForm;
