import _ from 'utils/i18n';


export const ConjunctionAnd = _('and');
export const ConjunctionOr = _('or');
export const ConjunctionNor = _('nor');

const Conjunctions = Object.freeze({
    And: ConjunctionAnd,
    Or: ConjunctionOr,
    Nor: ConjunctionNor,
});

export default Conjunctions;
