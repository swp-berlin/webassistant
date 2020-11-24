import 'styles/index.scss';

import {render} from 'react-dom';

import App from 'components/App';

const AppNode = document.getElementById('app');
const CSRFMiddlewareTokenNode = AppNode.getElementsByTagName('input')[0];
export const CSRFMiddlewareToken = CSRFMiddlewareTokenNode.value;

render(
    <App CSRFMiddlewareToken={CSRFMiddlewareToken} />,
    AppNode,
);
