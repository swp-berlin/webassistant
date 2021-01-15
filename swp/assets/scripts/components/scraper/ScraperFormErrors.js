import {useEffect, useState} from 'react';


const ScraperFormErrors = ({form, errors}) => {
    const [nonFieldErrors, setNonFieldErrors] = useState(errors && errors.non_field_errors);

    useEffect(() => {
        if (errors && errors.non_field_errors) {
            setNonFieldErrors(errors.non_field_errors);
            form.clearErrors('non_field_errors');
        }
    }, [form, errors]);

    if (!nonFieldErrors) return null;

    return (
        <ul className="my-8">
            {Object.values(nonFieldErrors).map(error => <li className="text-red-600">{error}</li>)}
        </ul>
    );
};

export default ScraperFormErrors;
