import _ from 'utils/i18n';
import BackButton from './BackButton';


const Label = _('Cancel');

const CancelButton = ({...props}) => (
    <BackButton {...props} />
);

CancelButton.defaultProps = {
    to: '..',
    text: Label,
    icon: '',
};

export default CancelButton;
