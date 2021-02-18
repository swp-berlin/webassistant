import {useEffect, useRef, useState} from 'react';
import PropTypes from 'prop-types';

const {createPortal} = require('react-dom');


const Portal = ({children, id}) => {
    const [mounted, setMounted] = useState(false);
    const node = useRef(null);

    useEffect(() => {
        node.current = document.getElementById(id);
        setMounted(true);
    }, [id]);

    if (!mounted || !node.current) return null;

    return createPortal(children, node.current);
};

Portal.propTypes = {
    selector: PropTypes.string,
};

Portal.defaultProps = {
    selector: 'body',
};

export default Portal;
