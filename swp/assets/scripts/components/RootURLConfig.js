import {Switch} from 'react-router-dom';

import SimpleRoute from 'components/SimpleRoute';
import Homepage from 'components/Homepage';
import {MonitorAdd, MonitorDetail, MonitorEdit, MonitorList} from 'components/monitor';
import {ScraperAdd, ScraperEdit} from 'components/scraper';
import {ThinktankAdd, ThinktankDetail, ThinktankEdit, ThinktankList, ThinktankPublications} from 'components/thinktank';


const RootURLConfig = () => (
    <Switch>
        <SimpleRoute path="/" exact>
            <Homepage />
        </SimpleRoute>

        <SimpleRoute path="/monitor/" exact>
            <MonitorList />
        </SimpleRoute>
        <SimpleRoute path="/monitor/add/" exact>
            <MonitorAdd />
        </SimpleRoute>
        <SimpleRoute path="/monitor/:id/" exact>
            {({params}) => <MonitorDetail id={params.id} />}
        </SimpleRoute>
        <SimpleRoute path="/monitor/:id/edit" exact>
            {({params}) => <MonitorEdit id={params.id} />}
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
        <SimpleRoute path="/thinktank/:id/publications/" exact>
            {({params}) => <ThinktankPublications id={params.id} />}
        </SimpleRoute>
        <SimpleRoute path="/thinktank/:thinktankID/scraper/add" exact>
            {({params}) => <ScraperAdd thinktankID={params.thinktankID} />}
        </SimpleRoute>
        <SimpleRoute path="/thinktank/:thinktankID/scraper/:id/" exact>
            {({params}) => <ScraperEdit id={params.id} thinktankID={params.thinktankID} />}
        </SimpleRoute>
    </Switch>
);

export default RootURLConfig;
