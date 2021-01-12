import {Switch} from 'react-router-dom';

import SimpleRoute from 'components/SimpleRoute';
import Scraper from 'components/scraper/Scraper';
import {NewThinktank, ThinktankEdit, ThinktankList} from 'components/thinktank';


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
