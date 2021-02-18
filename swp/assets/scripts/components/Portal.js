import {useEffect, useState} from 'react';
import PropTypes from 'prop-types';

const {createPortal} = require('react-dom');


const Portal = ({children, id}) => {
    const [currentID, setCurrentID] = useState();

    useEffect(() => setCurrentID(id), [id]);

    const node = document.getElementById(currentID || id);

    if (!node) return null;

    return createPortal(children, node);
};

Portal.propTypes = {
    id: PropTypes.string,
};

Portal.defaultProps = {
    id: 'body',
};

export default Portal;
