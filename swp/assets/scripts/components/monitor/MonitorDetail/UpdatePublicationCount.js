import {useCallback, useEffect} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faSync} from '@fortawesome/free-solid-svg-icons/faSync';

import {useMutation} from 'hooks/query';

const Action = 'update-publication-count';

const UpdatePublicationCount = ({id, onMonitorUpdate, children}) => {
    const [mutate, {loading, success}] = useMutation(`/monitor/${id}/${Action}/`);
    const handleClick = useCallback(
        event => {
            event.preventDefault();
            mutate({});
        },
        [mutate],
    );

    useEffect(() => { if (success) onMonitorUpdate(); }, [success, onMonitorUpdate]);

    return (
        <div className={Action}>
            {children}
            <button type="button" onClick={handleClick} disabled={loading}>
                <FontAwesomeIcon icon={faSync} />
            </button>
        </div>
    );
};

export default UpdatePublicationCount;
