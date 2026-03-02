import {useState} from 'react';

import {Button, Intent} from '@blueprintjs/core';

import Portal from 'components/Portal';

import _ from 'utils/i18n';

const SubmitButtonLabel = _('Save');
const Next = _('Next');
const Back = _('Back');

const MODAL_STYLE = {
    position: 'absolute',
    background: '#fff',
    boxShadow: '0px 8px 25px 15px #d1d5dbfd',
    left: '50%',
    top: '50%',
    transform: 'translate(-50%, -50%)',
    zIndex: '1000',
};

const CONTENT_STYLE = {
    margin: '2rem',
    overflow: 'scroll',
    minHeight: 'fit-content',
    maxHeight: '66vh',
};

export const MultiStepDialog = ({open, children, onClose, totalSteps, style, submitformID}) => {
    const [step, setSteps] = useState(1);

    if (!open) return null;

    function handlePrev() {
        if (step > 1) {
            setSteps(step => step - 1);
        }
    }

    function handleNext() {
        if (step < totalSteps) {
            setSteps(step => step + 1);
        }
    }

    const renderSteps = () => {
        if (step > 0 && step <= totalSteps) {
            return children[step - 1];
        }
        return null;
    };

    return (
        <Portal>
            <div style={{...MODAL_STYLE, ...style}}>
                <Button small minimal onClick={onClose} icon="cross" className="absolute top-5 right-5" />
                <div className="content" style={CONTENT_STYLE}>
                    {renderSteps()}
                </div>
                <div className="footer flex justify-center my-2">
                    <Button onClick={handlePrev} disabled={step <= 1}>
                        {Back}
                    </Button>
                    {step !== totalSteps
                        ? <Button onClick={handleNext} text={Next} />
                        : <Button text={SubmitButtonLabel} type="submit" form={submitformID} intent={Intent.PRIMARY} />
                    }
                </div>
            </div>
        </Portal>
    );
};
