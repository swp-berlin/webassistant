import 'styles/index.scss';

import {render} from 'react-dom';

import App from 'components/App';
import {CSRFMiddlewareToken} from 'utils/csrf';

const AppNode = document.getElementById('app');

render(
    <App CSRFMiddlewareToken={CSRFMiddlewareToken} />,
    AppNode,
);
