import {QueryClientProvider} from 'react-query';
import {ReactQueryDevtools} from 'react-query/devtools';
import {BrowserRouter as Router} from 'react-router-dom';

import queryClient from 'utils/react-query';

import Navigation from 'components/Navigation';
import RootURLConfig from 'components/RootURLConfig';

export default () => (
    <QueryClientProvider client={queryClient}>
        {process.env.NODE_ENV === 'production' || <ReactQueryDevtools />}
        <div className="container mx-auto my-16 px-4 py-4">
            <Router>
                <Navigation>
                    <RootURLConfig />
                </Navigation>
            </Router>
        </div>
    </QueryClientProvider>
);
