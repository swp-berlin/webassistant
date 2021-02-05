import {useEffect, useState} from 'react';


const ScraperFormErrors = ({form, errors}) => {
    const [dataErrors, setDataErrors] = useState(errors && errors.data);

    useEffect(() => {
        if (errors && errors.data) {
            setDataErrors(errors.data);
            form.clearErrors('data');
        }
    }, [form, errors]);

    if (!dataErrors) return null;

    return (
        <ul className="my-8">
            {Object.keys(dataErrors).filter(key => key !== 'ref').map(key => (
                <li key={key} className="text-red-600">{dataErrors[key]}</li>
            ))}
        </ul>
    );
};

export default ScraperFormErrors;
