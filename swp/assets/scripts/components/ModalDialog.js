import {Button} from '@blueprintjs/core';

import {useState} from 'react';
import Portal from 'components/Portal';

const MODAL_STYLE = {
    position: 'absolute',
    background: '#eeed',
    left: '50%',
    top: '50%',
    transform: 'translate(-50%, -50%)',
}

const CLOSE_BTN_STYLE = {
    margin: 0,
    top: '0px',
    right: '0px',
    border: 'none',
    background: 0,
    boxShadow: 'none',
    position: 'absolute',
}

const HEADER_STYLE = {
    margin: '1rem',
    top: '0',
}

const CONTENT_STYLE = {
    margin: '1rem',
}

const FOOTER_STYLE = {
    margin: '1rem',
    bottom: '0',
    right: '0',
}

export function MultiStepDialog({open, children, onClose, onFinalize, id}) {
    if (!open) return null;

    const [step, setSteps] = useState(1);
    const totalSteps = 2;

    function handlePrev() {
        if (step > 1)
            setSteps((step) => step - 1);
    }

    function handleNext() {
        if (step < totalSteps)
            setSteps((step) => step + 1);
    }

    const renderSteps = () => {
        switch (step) {
            case 1:
                return children[0];
            case 2:
                return children[1];
            default:
                return null;
        }
    }

    if (open) return (
        <Portal>
            <div style={MODAL_STYLE}>
                <Button onClick={onClose} style={CLOSE_BTN_STYLE}> X </Button>
                <div className="header"  style={HEADER_STYLE}>
                    Header
                </div>
                <div className="content" style={CONTENT_STYLE}>
                    {renderSteps()}
                </div>
                <div className="footer" style={FOOTER_STYLE}>
                    {step > 1 ?
                        <Button onClick={handlePrev}>
                            Zurück
                        </Button> : null
                    }
                    {step !== totalSteps ?
                        <Button onClick={handleNext}>
                            Weiter
                        </Button> :
                        <Button onClick={onFinalize}>
                            Hinzufügen
                        </Button>
                    }
                </div>
            </div>
        </Portal>
    );
}
