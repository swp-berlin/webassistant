import {Button} from '@blueprintjs/core';
import {DateRangePicker as BPDateRangePicker} from '@blueprintjs/datetime';
import {Classes, Popover2} from '@blueprintjs/popover2';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCalendar} from '@fortawesome/free-solid-svg-icons/faCalendar';
import format from 'date-fns/format';

import _ from 'utils/i18n';
import {useState} from 'react';

const SinceLabel = _('since');
const UntilLabel = _('until');

const formatDate = date => date && format(date, 'dd.MM.yyyy', {representation: 'date'});

const getDateRepresentation = ([startDate, endDate]) => {
    if (!startDate && !endDate) return '';
    if (startDate && !endDate) return `${SinceLabel} ${formatDate(startDate)}`;
    if (endDate && !startDate) return `${UntilLabel} ${formatDate(endDate)}`;

    return `${formatDate(startDate)} ${UntilLabel} ${formatDate(endDate)}`;
};

const DateRangePicker = ({defaultValue, onChange}) => {
    const [dates, setDates] = useState([null, null]);
    const handleChange = dates => {
        setDates(dates);
        onChange(dates);
    };

    return (
        <Popover2
            interactionKind="click"
            popoverClassName={Classes.POPOVER2_CONTENT_SIZING}
            placement="bottom-start"
            content={<BPDateRangePicker defaultValue={defaultValue} onChange={handleChange} />}
        >
            <Button minimal icon={<FontAwesomeIcon icon={faCalendar} />} text={getDateRepresentation(dates)} />
        </Popover2>
    );
};

export default DateRangePicker;
