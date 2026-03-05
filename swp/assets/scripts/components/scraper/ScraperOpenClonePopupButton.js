import {useState} from 'react';

import {useParams} from 'react-router-dom';

import {Button} from '@blueprintjs/core';

import _ from 'utils/i18n';

import {MultiStepDialog} from 'components/ModalDialog';
import Query from 'components/Query';

import ScraperClone from './ScraperClone';

const ChooseThinktank = _('Select a thinktank for the new scraper.');
const SELECT_STYLE = {
    padding: '.75rem 1.5rem',
    fontSize: 'large',
    border: '1px solid gray',
    borderRadius: '2px',
    background: 'transparent',
};

const CLONEFORM_STYLE = {
    width: 'min(100%, 1200px)',
};

const SelectThinktank = ({thinktankID, onChange}) => (
    <>
        <h4>{ChooseThinktank}</h4>
        <div className="flex justify-center my-5">
            <Query queryKey={['thinktank']}>
                { thinktanks => (
                    <select defaultValue={thinktankID} onChange={onChange} style={SELECT_STYLE}>
                        {thinktanks.map(thinktank => (
                            <option key={thinktank.id} value={thinktank.id}>{thinktank.name}</option>
                        ))}
                    </select>
                )}
            </Query>
        </div>
    </>
);

function OpenCloneScraperPopupButton({scraperID}) {
    const {id} = useParams();
    const [isOpen, setIsOpen] = useState(false);
    const [selectedThinktankID, setSelectedThinktankID] = useState(id);
    const endpoint = `/thinktank/${id}/`;

    return (
        <>
            <Button onClick={() => { setIsOpen(true); setSelectedThinktankID(id); }}>⧉</Button>
            <MultiStepDialog
                open={isOpen}
                onClose={() => setIsOpen(false)}
                onFinalize={() => setIsOpen(false)}
                totalSteps={2}
                style={CLONEFORM_STYLE}
                submitformID="scrapercloneform"
            >
                <SelectThinktank
                    thinktankID={selectedThinktankID}
                    onChange={e => setSelectedThinktankID(e.target.value)}
                />
                <ScraperClone
                    endpoint={endpoint}
                    thinktankID={selectedThinktankID}
                    scraperID={scraperID}
                    onSuccess={() => setIsOpen(false)}
                />
            </MultiStepDialog>
        </>
    );
}

export default OpenCloneScraperPopupButton;
