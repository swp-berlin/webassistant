import {useMemo} from 'react';
import PropTypes from 'prop-types';
import Conjunctions from './Conjunctions';


const generateSeparators = (count, conjunction, delimiter = ',') => {
    const separator = `${delimiter} `;
    const finalSeparator = conjunction ? ` ${conjunction} ` : separator;
    return new Array(count)
        .fill(finalSeparator, count - 1, count)
        .fill(separator, 1, count - 1)
        .fill('', 0, 1);
};

const CommaList = ({items, conjunction, delimiter, ...props}) => {
    const separators = useMemo(
        () => generateSeparators(items.length, conjunction, delimiter),
        [items.length, conjunction, delimiter],
    );

    return (
        <ul className="inline list-inline" {...props}>
            {items.map((item, i) => (
                // eslint-disable-next-line react/no-array-index-key
                <li key={i}>
                    {separators[i]}
                    {item}
                </li>
            ))}
        </ul>
    );
};

CommaList.defaultProps = {
    conjunction: Conjunctions.And,
    delimiter: ',',
};

CommaList.propTypes = {
    conjunction: PropTypes.string,
    delimiter: PropTypes.string,
};

export default CommaList;
