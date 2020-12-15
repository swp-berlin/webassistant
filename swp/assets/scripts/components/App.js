import {BrowserRouter as Router} from 'react-router-dom';

import RootURLConfig from 'components/RootURLConfig';

export default () => (
    <div className="container mx-auto my-8 py-4">
        <Router>
            <RootURLConfig />
        </Router>
    </div>
);
