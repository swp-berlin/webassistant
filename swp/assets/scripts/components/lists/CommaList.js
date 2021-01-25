import PropTypes from 'prop-types';
import _ from 'utils/i18n';


const And = _('and');

const CommaList = ({children, alwaysUseComma, ...props}) => {
    const last = children.length - 1;
    const chooseSeparator = i => (!alwaysUseComma && i < last ? ',' : ` ${And}`);

    return (
        <ul className="inline list-inline" {...props}>
            {children.map((item, i) => (
                <li key={item}>
                    {i > 0 ? `${chooseSeparator(i)} ${item}` : item}
                </li>
            ))}
        </ul>
    );
};

CommaList.defaultProps = {
    alwaysUseComma: false,
};

CommaList.propTypes = {
    alwaysUseComma: PropTypes.bool,
};

export default CommaList;
