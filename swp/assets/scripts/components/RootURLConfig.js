import {Switch} from 'react-router-dom';

import Scraper from 'components/scraper/Scraper';
import ThinktankList from 'components/thinktank/ThinktankList';

import SimpleRoute from 'components/SimpleRoute';


const RootURLConfig = () => (
    <Switch>
        <SimpleRoute path="/" exact>
            {() => <p>Hello World!</p>}
        </SimpleRoute>
        <SimpleRoute path="/scraper/:id/" exact>
            {({params}) => <Scraper id={params.id} />}
        </SimpleRoute>
        <SimpleRoute path="/thinktank/" exact>
            <ThinktankList />
        </SimpleRoute>
    </Switch>
);

export default RootURLConfig;
