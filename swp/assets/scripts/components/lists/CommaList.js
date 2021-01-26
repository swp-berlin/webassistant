import PropTypes from 'prop-types';
import _ from 'utils/i18n';


const And = _('and');
const Or = _('or');

const CommaList = ({items, alwaysUseComma, endWithOr, ...props}) => {
    const last = items.length - 1;
    const lastWord = endWithOr ? Or : And;
    const finalSeparator = alwaysUseComma ? ',' : ` ${lastWord}`;

    const chooseSeparator = i => (i < last ? ',' : finalSeparator);

    return (
        <ul className="inline list-inline" {...props}>
            {items.map((item, i) => (
                // eslint-disable-next-line react/no-array-index-key
                <li key={i}>{i > 0 ? `${chooseSeparator(i)} ${item}` : item}</li>
            ))}
        </ul>
    );
};

CommaList.defaultProps = {
    alwaysUseComma: false,
    endWithOr: false,
};

CommaList.propTypes = {
    alwaysUseComma: PropTypes.bool,
    endWithOr: PropTypes.bool,
};

export default CommaList;
