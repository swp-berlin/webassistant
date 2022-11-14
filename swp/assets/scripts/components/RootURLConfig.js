import {Switch} from 'react-router-dom';

import SimpleRoute from 'components/SimpleRoute';
import Homepage from 'components/Homepage';
import {MonitorAdd, MonitorDetail, MonitorEdit, MonitorList, MonitorNewPublications, MonitorPublications} from 'components/monitor';
import {ScraperAdd, ScraperEdit} from 'components/scraper';
import {ThinktankAdd, ThinktankDetail, ThinktankEdit, ThinktankList, ThinktankPublications} from 'components/thinktank';
import {ThinktankFilterAdd, ThinktankFilterEdit} from 'components/thinktankfilter';
import {PublicationList, PublicationListDetail} from 'components/publication-list';


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
        <SimpleRoute path="/monitor/:id/filter/add/" exact>
            {({params}) => <ThinktankFilterAdd monitorID={params.id} />}
        </SimpleRoute>
        <SimpleRoute path="/monitor/:monitorID/filter/:id/edit/" exact>
            {({params}) => <ThinktankFilterEdit monitorID={params.monitorID} id={params.id} />}
        </SimpleRoute>
        <SimpleRoute path="/monitor/:id/publications/" exact>
            {({params}) => <MonitorPublications id={params.id} />}
        </SimpleRoute>
        <SimpleRoute path="/monitor/:id/publications/new/" exact>
            {({params}) => <MonitorNewPublications id={params.id} />}
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

        <SimpleRoute path="/publication-list/" exact>
            {({url}) => <PublicationList url={url} />}
        </SimpleRoute>
        <SimpleRoute path="/publication-list/:id/" exact>
            {({url, params}) => <PublicationListDetail id={+params.id} url={url} />}
        </SimpleRoute>
    </Switch>
);

export default RootURLConfig;
