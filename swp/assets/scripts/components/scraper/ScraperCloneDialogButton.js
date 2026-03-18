import {useCallback, useState} from 'react';
import {useQueryClient} from 'react-query';

import {Button, DialogStep, Intent, MultistepDialog} from '@blueprintjs/core';

import _ from 'utils/i18n';
import {preventDefault} from 'utils/event';

import Query from 'components/Query';

import ScraperCloneForm, {ScraperCloneFormID} from './ScraperCloneForm';

const Clone = _('Clone');
const Title = _('Clone Scraper');
const SelectThinktankTitle = _('Select Thinktank');
const SubmitButtonLabel = _('Save');
const Next = _('Next');
const Back = _('Back');

const SelectThinktank = ({thinktankID, onChange}) => (
    <div className="flex justify-center my-5">
        <Query queryKey={['thinktank']}>
            {thinktanks => (
                <select
                    className="px-4 py-4 text-lg rounded-sm bg-white"
                    defaultValue={thinktankID}
                    onChange={onChange}
                >
                    {thinktanks.map(thinktank => (
                        <option key={thinktank.id} value={thinktank.id}>{thinktank.name}</option>
                    ))}
                </select>
            )}
        </Query>
    </div>
);

const ScraperCloneDialogButton = ({scraperID, thinktankID}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedThinktankID, setSelectedThinktankID] = useState(thinktankID);
    const handleClick = useCallback(
        event => {
            preventDefault(event);
            setIsOpen(true);
            setSelectedThinktankID(thinktankID);
        },
        [thinktankID],
    );
    const handleClose = useCallback(() => setIsOpen(false), []);
    const handleThinktankSelect = useCallback(
        event => {
            setSelectedThinktankID(event.target.value);
        },
        [],
    );
    const queryClient = useQueryClient();
    const handleSuccess = useCallback(
        async ({thinktank}) => {
            await queryClient.invalidateQueries(['thinktank', thinktank.id]);

            return setIsOpen(false);
        },
        [queryClient],
    );

    return (
        <>
            <Button text={Clone} icon="duplicate" onClick={handleClick} />
            <MultistepDialog
                className="scraper-clone-dialog"
                backButtonProps={{
                    text: Back,
                }}
                nextButtonProps={{
                    text: Next,
                }}
                finalButtonProps={{
                    intent: Intent.PRIMARY,
                    text: SubmitButtonLabel,
                    form: ScraperCloneFormID,
                    type: 'submit',
                }}
                isOpen={isOpen}
                // navigationPosition="top" // Doesn't seem to work. See styles/scraper-clone-dialog.scss
                onClose={handleClose}
                title={Title}
            >
                <DialogStep
                    id="select"
                    title={SelectThinktankTitle}
                    panel={(
                        <SelectThinktank
                            thinktankID={selectedThinktankID}
                            onChange={handleThinktankSelect}
                        />
                    )}
                />
                <DialogStep
                    id="confirm"
                    panel={(
                        <ScraperCloneForm
                            thinktankID={selectedThinktankID}
                            scraperID={scraperID}
                            redirectURL={`/thinktank/${thinktankID}/`}
                            onSuccess={handleSuccess}
                        />
                    )}
                    title={Title}
                />
            </MultistepDialog>
        </>
    );
};

export default ScraperCloneDialogButton;
