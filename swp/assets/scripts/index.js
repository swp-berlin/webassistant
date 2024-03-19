import 'styles/index.scss';

import {render} from 'react-dom';

import {CSRFMiddlewareToken} from 'utils/csrf';

import App from 'components/App';

const AppNode = document.getElementById('app');

render(
    <App CSRFMiddlewareToken={CSRFMiddlewareToken} />,
    AppNode,
);
