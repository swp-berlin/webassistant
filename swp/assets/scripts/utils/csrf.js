const AppNode = document.getElementById('app');
const CSRFMiddlewareTokenNode = AppNode.getElementsByTagName('input')[0];

export const CSRFMiddlewareToken = CSRFMiddlewareTokenNode.value;
