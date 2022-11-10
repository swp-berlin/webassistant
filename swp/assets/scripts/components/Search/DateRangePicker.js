import {Button} from '@blueprintjs/core';
import {DateRangePicker as BPDateRangePicker} from '@blueprintjs/datetime';
import {Classes, Popover2} from '@blueprintjs/popover2';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCalendar} from '@fortawesome/free-solid-svg-icons/faCalendar';

const DateRangePicker = ({defaultValue, onChange}) => (
    <Popover2
        interactionKind="click"
        popoverClassName={Classes.POPOVER2_CONTENT_SIZING}
        placement="bottom-start"
        content={<BPDateRangePicker defaultValue={defaultValue} onChange={onChange} />}
    >
        <Button minimal icon={<FontAwesomeIcon icon={faCalendar} />} />
    </Popover2>
);

export default DateRangePicker;
