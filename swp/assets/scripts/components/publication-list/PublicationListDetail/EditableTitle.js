/* eslint-disable default-case */

import {useCallback, useEffect, useRef, useState} from 'react';
import {Icon} from '@blueprintjs/core';

import {useMutationResult} from 'components/Fetch';

const Enter = 'Enter';
const Escape = 'Escape';

const preventEnter = event => {
    if (event.key === Enter) event.preventDefault();
};

const EditableTitle = ({id, title, setTitle}) => {
    const inputRef = useRef(null);
    const [isEditing, setIsEditing] = useState(false);
    const endpoint = `/publication-list/${id}/`;
    const [mutate, {loading}] = useMutationResult(endpoint, {}, []);

    const handleClick = useCallback(
        () => {
            if (loading) return;

            if (isEditing) {
                const title = inputRef.current.innerText;
                if (title) setTitle(title);
                mutate({name: title}, 'PATCH');
                setIsEditing(false);
            } else {
                setIsEditing(true);
            }
        },
        [isEditing, loading, mutate, setTitle, setIsEditing, inputRef],
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
