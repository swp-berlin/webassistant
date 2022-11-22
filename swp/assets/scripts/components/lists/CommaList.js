import {useMemo} from 'react';
import PropTypes from 'prop-types';
import cN from 'classnames';

import Conjunctions from './Conjunctions';


const generateSeparators = (count, conjunction, delimiter = ',') => {
    const separator = `${delimiter} `;
    const finalSeparator = conjunction ? ` ${conjunction} ` : separator;
    return new Array(count)
        .fill(finalSeparator, count - 1, count)
        .fill(separator, 1, count - 1)
        .fill('', 0, 1);
};

const CommaList = ({className, inline, items, conjunction, delimiter, ...props}) => {
    const separators = useMemo(
        () => generateSeparators(items.length, conjunction, delimiter),
        [items.length, conjunction, delimiter],
    );

    return (
        <ul className={cN('list-inline pl-0', className, {inline})} {...props}>
            {items.map((item, i) => (
                // eslint-disable-next-line react/no-array-index-key
                <li className="inline" key={i}>
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
