import {Switch} from 'react-router-dom';

import Scraper from 'components/scraper/Scraper';
import ThinktankList from 'components/thinktank/ThinktankList';

import SimpleRoute from 'components/SimpleRoute';
import NewThinktank from 'components/thinktank/NewThinktank';
import ThinktankEdit from 'components/thinktank/ThinktankEdit';


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
        <SimpleRoute path="/thinktank/new/" exact>
            <NewThinktank />
        </SimpleRoute>
        <SimpleRoute path="/thinktank/:id/edit/" exact>
            {({params}) => <ThinktankEdit id={params.id} />}
        </SimpleRoute>
    </Switch>
);

export default RootURLConfig;
