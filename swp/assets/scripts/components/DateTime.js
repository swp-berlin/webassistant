import PropTypes from 'prop-types';

import dateformat from 'utils/dateformat';


const DateTime = ({value, pattern, empty}) => (
    value ? <time dateTime={value}>{dateformat(value, pattern)}</time> : empty
);

DateTime.defaultProps = {
    value: null,
    empty: '—',
    pattern: 'P p',
};

DateTime.propTypes = {
    value: PropTypes.oneOfType([
        PropTypes.instanceOf(Date),
        PropTypes.string,
    ]),
    pattern: PropTypes.string,
    empty: PropTypes.string,
};

export default DateTime;
