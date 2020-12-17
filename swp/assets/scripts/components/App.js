import {BrowserRouter as Router} from 'react-router-dom';

import Navigation from 'components/Navigation';
import RootURLConfig from 'components/RootURLConfig';

export default () => (
    <div className="container mx-auto my-16 py-4">
        <Router>
            <Navigation>
                <RootURLConfig />
            </Navigation>
        </Router>
    </div>
);
