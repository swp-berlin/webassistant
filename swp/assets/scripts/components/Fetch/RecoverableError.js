import ReloadButton from './ReloadButton';
import BaseError from './BaseError';

const RecoverableError = ({reload, ...props}) => {
    const action = <ReloadButton reload={reload} />;

    return (<BaseError action={action} {...props} />);
};

export default RecoverableError;
