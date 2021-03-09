/* eslint-disable no-use-before-define */

import {isValidElement} from 'react';
import {Route} from 'react-router-dom';
import PropTypes from 'prop-types';

const SimpleRoute = ({children, always, ...props}) => (
    <Route {...props}>
        {buildRender(children, always)}
    </Route>
);

const buildRender = (children, always) => ({match, location, history}) => (
    Boolean(always || match) && render(children, match, location, history)
);

const render = (children, match, location, history) => (
    isValidElement(children) ? children : children(match, location, history)
);

SimpleRoute.propTypes = {
    ...Route.propTypes,
    children: PropTypes.oneOfType([
        PropTypes.func,
        PropTypes.element,
    ]).isRequired,
    always: PropTypes.bool,
};

SimpleRoute.defaultProps = {
    always: false,
};

export default SimpleRoute;
