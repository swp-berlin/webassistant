import {useCallback, useRef} from 'react';
import {useQueryClient} from 'react-query';
import {Button, ControlGroup} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {buildAPIURL} from 'utils/api';
import {getClientErrors, isBadRequest} from 'utils/react-query-fetch';

import {useMutation} from 'hooks/react-query';

import {TextInput} from 'components/forms';

const Method = 'POST';
const SubmitLabel = _('Add');
const Placeholder = _('Add a new publication list…');
const ErrorMessage = _('Publication list could not be added.');

const PublicationListAddForm = ({endpoint}) => {
    const inputRef = useRef(null);
    const url = buildAPIURL(endpoint);
    const queryClient = useQueryClient();
    const {mutate, error} = useMutation(url, Method, {
        onSuccess(data) {
            inputRef.current.value = '';
            queryClient.setQueryData(endpoint, publicationLists => ([data, ...publicationLists]));
        },
        onError(error) {
            if (isBadRequest(error)) return ErrorMessage;
        },
    });
    const handleSubmit = useCallback(
        event => {
            event.preventDefault();
            mutate({name: inputRef.current.value});
        },
        [mutate],
    );
    const clientErrors = getClientErrors(error);

    return (
        <form action={url} method={Method} onSubmit={handleSubmit}>
            <ControlGroup>
                <TextInput
                    name="name"
                    placeholder={Placeholder}
                    errors={clientErrors}
                    inputRef={inputRef}
                />
                <Button type="submit" text={SubmitLabel} />
            </ControlGroup>
        </form>
    );
};

export default PublicationListAddForm;
