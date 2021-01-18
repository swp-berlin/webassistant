import {Switch} from 'react-router-dom';

import SimpleRoute from 'components/SimpleRoute';
import Homepage from 'components/Homepage';
import {ScraperDetail} from 'components/scraper';
import {ThinktankAdd, ThinktankDetail, ThinktankEdit, ThinktankList} from 'components/thinktank';


const RootURLConfig = () => (
    <Switch>
        <SimpleRoute path="/" exact>
            <Homepage />
        </SimpleRoute>
        <SimpleRoute path="/scraper/:id/" exact>
            {({params}) => <ScraperDetail id={params.id} />}
        </SimpleRoute>
        <SimpleRoute path="/thinktank/" exact>
            <ThinktankList />
        </SimpleRoute>
        <SimpleRoute path="/thinktank/add/" exact>
            <ThinktankAdd />
        </SimpleRoute>
        <SimpleRoute path="/thinktank/:id/" exact>
            {({params}) => <ThinktankDetail id={params.id} />}
        </SimpleRoute>
        <SimpleRoute path="/thinktank/:id/edit/" exact>
            {({params}) => <ThinktankEdit id={params.id} />}
        </SimpleRoute>
    </Switch>
);

export default RootURLConfig;
