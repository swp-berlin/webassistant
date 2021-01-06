import parseISO from 'date-fns/parseISO';
import format from 'date-fns/format';
import {de} from 'date-fns/locale';


const dateformat = (date, pattern, locale = de) => format(parseISO(date), pattern || 'P p', {locale});


export default dateformat;
