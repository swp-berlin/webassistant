import {useCallback} from 'react';
import {DateInput as BPDateInput} from '@blueprintjs/datetime';
import {Controller} from 'react-hook-form';
import addYears from 'date-fns/addYears';
import format from 'date-fns/format';
import formatISO from 'date-fns/formatISO';
import isAfter from 'date-fns/isAfter';
import isBefore from 'date-fns/isBefore';
import isValid from 'date-fns/isValid';
import parse from 'date-fns/parse';
import parseISO from 'date-fns/parseISO';
import subDays from 'date-fns/subDays';

import _, {interpolate} from 'utils/i18n';

import Field from './Field';


const DATE_FORMAT = 'dd.MM.yyyy';
const DEFAULT_MIN_DATE = parseISO('1900-01-01');
const DEFAULT_MAX_DATE = addYears(new Date(), 100);

const InvalidDateMessage = interpolate(_('Please enter a valid date in the format %(format)s'), {format: DATE_FORMAT});

const parseInput = (date, initial) => {
    const parsed = parse(date, DATE_FORMAT, initial);
    return isValid(parsed) && parsed;
};

const isBetween = (date, min, max) => isAfter(date, subDays(min, 1)) && isBefore(date, subDays(max, 1));

const DateInput = ({onChange, inputProps, value, defaultValue, minDate, maxDate, ...props}) => {
    const handleChange = useCallback(date => {
        if (isValid(date) && isBetween(date, minDate, maxDate)) onChange(date);
        else onChange(null);
    }, [maxDate, minDate, onChange]);

    return (
        <BPDateInput
            {...props}
            value={value && parseISO(value)}
            minDate={minDate}
            maxDate={maxDate}
            defaultValue={defaultValue && parseISO(defaultValue)}
            onChange={handleChange}
            formatDate={date => format(date, DATE_FORMAT)}
            parseDate={date => parseInput(date, defaultValue ? parseISO(defaultValue) : new Date())}
            inputProps={inputProps}
        />
    );
};

DateInput.defaultProps = {
    minDate: DEFAULT_MIN_DATE,
    maxDate: DEFAULT_MAX_DATE,
};

const DateInputField = ({control, id, name, formatDate, ...props}) => (
    <Field id={id} name={name} {...props}>
        <Controller
            as={DateInput}
            control={control}
            rules={{validate: date => isValid(parseISO(date)) || InvalidDateMessage}}
            name={name}
            onChange={([date]) => date && (formatDate ? formatDate(date) : formatISO(date, {representation: 'date'}))}
            inputProps={{id}}
            fill
        />
    </Field>
);

export default DateInputField;
