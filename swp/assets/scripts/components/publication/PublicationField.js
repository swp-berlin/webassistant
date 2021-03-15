import {Icon} from '@blueprintjs/core';
import cN from 'classnames';

import {getChoices} from 'utils/choices';


const KeyChoices = getChoices('DataResolverKey');

const getLabel = name => {
    const choice = KeyChoices.find(choice => choice.value === name);

    if (choice) return choice.label;

    return name;
};

const PublicationFieldError = ({className, name, error: {message, level}}) => (
    <div className={cN('p-2 text-yellow-400 border-yellow-400 border-2', className)}>
        <Icon icon={level === 'Warning' ? 'warning-sign' : 'error'} />
        <span className="pl-2">{`${getLabel(name)}:`}</span>
        <span className="pl-2">{message}</span>
    </div>
);

const PublicationField = ({className, name, value, children}) => {
    if (typeof value === 'object' && value?.message) {
        return <PublicationFieldError className={className} name={name} error={value} />;
    }

    return children;
};

export default PublicationField;
