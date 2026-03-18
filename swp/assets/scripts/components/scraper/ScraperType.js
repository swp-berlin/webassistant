import {getChoices} from 'utils/choices';

export const ScraperTypes = getChoices('ScraperType');

const ScraperTypeLabels = Object.fromEntries(ScraperTypes.map(({value, label}) => [value, label]));

const ScraperType = ({type}) => ScraperTypeLabels[type] || type;

export default ScraperType;
