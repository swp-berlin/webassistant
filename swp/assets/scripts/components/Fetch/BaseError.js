import {NonIdealState} from '@blueprintjs/core';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';


const BaseError = ({status, Errors, Fallback, ...props}) => {
    const defaultProps = Errors[status] || Fallback;
    const icon = <FontAwesomeIcon icon={defaultProps.icon} />;

    return (<NonIdealState {...defaultProps} icon={icon} {...props} />);
};

BaseError.defaultProps = {
    Errors: {},
};

export default BaseError;
