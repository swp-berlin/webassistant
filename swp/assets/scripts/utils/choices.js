import Choices from 'schemes/choices';
import _ from 'utils/i18n';

export const translated = name => Choices[name].map(({label, ...choice}) => ({
    ...choice,
    label: _(label),
}));

export const getChoices = name => translated(name);

export const getLabel = (name, value) => {
    const choice = Choices[name].find(choice => choice.value === value);

    if (!choice) return value;

    const {label} = choice;

    return _(label);
};
