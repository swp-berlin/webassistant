import cN from 'classnames';


const Errors = ({errors, className}) => (
    <ul className={cN('field-errors', className)}>
        {Object.keys(errors.types).map(code => (
            <li key={code}>{errors.types[code]}</li>
        ))}
    </ul>
);

export default Errors;
