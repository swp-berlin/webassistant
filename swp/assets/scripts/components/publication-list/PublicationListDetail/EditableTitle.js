/* eslint-disable default-case */

import {useCallback, useEffect, useRef, useState} from 'react';
import {useQueryClient} from 'react-query';
import {Icon} from '@blueprintjs/core';

import {buildAPIURL} from 'utils/api';
import {getClientErrors, isBadRequest} from 'utils/react-query-fetch';

import {useMutation} from 'hooks/react-query';

import {Endpoint} from '../PublicationList';

const Enter = 'Enter';
const Escape = 'Escape';

const preventEnter = event => {
    if (event.key === Enter) event.preventDefault();
};

const EditableTitle = ({id, title}) => {
    const inputRef = useRef(null);
    const [isEditing, setIsEditing] = useState(false);
    const queryKey = [Endpoint, id];
    const url = buildAPIURL(...queryKey);
    const queryClient = useQueryClient();
    const {mutate, isLoading} = useMutation(url, 'PATCH', {
        onSuccess(data) {
            setIsEditing(false);
            queryClient.setQueryData(queryKey, publicationList => ({...publicationList, ...data}));
        },
        onError(error) {
            if (isBadRequest(error)) return getClientErrors(error).name;
        },
    });

    const handleClick = useCallback(
        () => {
            if (isLoading) return;

            if (isEditing) {
                mutate({name: inputRef.current.innerText});
            } else {
                setIsEditing(true);
            }
        },
        [isEditing, isLoading, mutate, setIsEditing, inputRef],
    );

    const handleCancel = useCallback(
        () => {
            inputRef.current.innerText = title;
            setIsEditing(false);
        },
        [title, setIsEditing, inputRef],
    );

    const handleKeyUp = useCallback(
        event => {
            switch (event.key) {
                case Enter:
                    return handleClick();
                case Escape:
                    return handleCancel();
            }
        },
        [handleClick, handleCancel],
    );

    useEffect(
        () => {
            if (isEditing) {
                const range = document.createRange();
                const selection = window.getSelection();

                inputRef.current.focus();
                range.selectNodeContents(inputRef.current);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        },
        [isEditing, inputRef],
    );

    const props = {
        ref: inputRef,
        onKeyUp: handleKeyUp,
        onKeyPress: preventEnter,
        contentEditable: isEditing,
        suppressContentEditableWarning: isEditing,
    };

    return (
        <div className="flex items-center">
            <span className="outline-none" role="textbox" {...props}>{title}</span>
            <Icon className="mx-1" icon={isEditing ? 'floppy-disk' : 'edit'} onClick={handleClick} />
            {isEditing && <Icon icon="undo" onClick={handleCancel} />}
        </div>
    );
};

export default EditableTitle;
