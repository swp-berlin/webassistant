import cN from 'classnames';


const Errors = ({errors, className}) => (
    <ul className={cN('field-errors', className)}>
        {errors.map(({code, msg}) => (
            <li key={code}>{msg}</li>
        ))}
    </ul>
);

export default Errors;
