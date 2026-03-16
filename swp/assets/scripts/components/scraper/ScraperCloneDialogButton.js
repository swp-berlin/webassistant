import {useState} from 'react';

import {Button, DialogStep, Intent, MultistepDialog} from '@blueprintjs/core';

import _ from 'utils/i18n';

import Query from 'components/Query';

import ScraperCloneForm, {ScraperCloneFormID} from './ScraperCloneForm';

const Title = _('Clone Scraper');
const SelectThinktankTitle = _('Select Thinktank');
const SubmitButtonLabel = _('Save');
const Next = _('Next');
const Back = _('Back');

const SelectThinktank = ({thinktankID, onChange}) => (
    <div className="flex justify-center my-5">
        <Query queryKey={['thinktank']}>
            { thinktanks => (
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
    const endpoint = `/thinktank/${thinktankID}/`;
    const finalButtonProps = {
        intent: Intent.PRIMARY,
        onClick: () => setIsOpen(false),
        text: SubmitButtonLabel,
        form: ScraperCloneFormID,
        type: 'submit',
    };
    const backButtonProps = {
        text: Back,
    };
    const nextButtonProps = {
        text: Next,
    };

    return (
        <>
            <Button icon="duplicate" onClick={() => { setIsOpen(true); setSelectedThinktankID(thinktankID); }} />
            <MultistepDialog
                className="duplicate-scraper-dialog"
                backButtonProps={backButtonProps}
                nextButtonProps={nextButtonProps}
                finalButtonProps={finalButtonProps}
                isOpen={isOpen}
                // navigationPosition="top" // Doesn't seem to work. See styles/duplicate-scraper-dialog.scss
                onClose={() => setIsOpen(false)}
                title={Title}
            >
                <DialogStep
                    id="select"
                    title={SelectThinktankTitle}
                    panel={(
                        <SelectThinktank
                            thinktankID={selectedThinktankID}
                            onChange={e => setSelectedThinktankID(e.target.value)}
                        />
                    )}
                />
                <DialogStep
                    id="confirm"
                    panel={(
                        <ScraperCloneForm
                            endpoint={endpoint}
                            thinktankID={selectedThinktankID}
                            scraperID={scraperID}
                            onSuccess={() => setIsOpen(false)}
                        />
                    )}
                    title={Title}
                />
            </MultistepDialog>
        </>
    );
};

export default ScraperCloneDialogButton;
