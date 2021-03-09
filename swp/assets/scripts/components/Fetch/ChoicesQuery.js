import {cloneElement} from 'react';

import {useQuery} from 'hooks/query';

import defaultHandlers from './defaultHandler';
import getResult from './Result';

const prepareChoice = ({value, label, /* some common attributes: */ id, key, code, name, title}) => ({
    value: value || id || key || code,
    label: label || name || title,
});

const prepareChoices = (data, prepareChoice) => data.map(prepareChoice);

const ChoicesQuery = ({endpoint, params, defaultChoices, prepareChoices, prepareChoice, children}) => {
    const result = useQuery(endpoint, params);
    const childProps = {choices: defaultChoices, reload: result.fetch};

    const error = getResult({
        ...defaultHandlers,
        result,
        handleSuccess: data => {
            childProps.choices = prepareChoices(data, prepareChoice);
        },
    });

    if (error) childProps.noResults = <li className="choices-query">{error}</li>;

    return cloneElement(children, childProps);
};

ChoicesQuery.defaultProps = {
    prepareChoice,
    prepareChoices,
    defaultChoices: [],
};

export default ChoicesQuery;
