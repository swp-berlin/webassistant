import {Routes, Route} from 'react-router-dom';

import Homepage from 'components/Homepage';
import {
    MonitorAdd,
    MonitorDetail,
    MonitorEdit,
    MonitorList,
    MonitorNewPublications,
    MonitorPublications
} from 'components/monitor';
import {ScraperAdd, ScraperEdit} from 'components/scraper';
import {ThinktankAdd, ThinktankDetail, ThinktankEdit, ThinktankList, ThinktankPublications} from 'components/thinktank';
import {ThinktankFilterAdd, ThinktankFilterEdit} from 'components/thinktankfilter';
import SearchPage from 'components/Search/SearchPage';


const RootURLConfig = () => (
    <Routes>
        <Route path="/" element={<Homepage />} />

        <Route path="/monitor" element={<MonitorList />} />
        <Route path="/monitor/:id" element={<MonitorDetail />} />
        <Route path="/monitor/:id/edit" element={<MonitorEdit />} />
        <Route path="/monitor/add" element={<MonitorAdd />} />
        <Route path="/monitor/:id/filter/add/" element={<ThinktankFilterAdd />} />
        <Route path="/monitor/:monitorID/filter/:id/edit/" element={<ThinktankFilterEdit />} />
        <Route path="/monitor/:id/publications/" element={<MonitorPublications />} />
        <Route path="/monitor/:id/publications/new/" element={<MonitorNewPublications />} />

        <Route path="/thinktank/" element={<ThinktankList />} />
        <Route path="/thinktank/add/" element={<ThinktankAdd />} />
        <Route path="/thinktank/:id/" element={<ThinktankDetail />} />
        <Route path="/thinktank/:id/edit/" element={<ThinktankEdit />} />
        <Route path="/thinktank/:id/publications/" element={<ThinktankPublications />} />
        <Route path="/thinktank/:thinktankID/scraper/add" element={<ScraperAdd />} />
        <Route path="/thinktank/:thinktankID/scraper/:id/" element={<ScraperEdit />} />

        <Route path="/search/" element={<SearchPage />} />
    </Routes>
);

export default RootURLConfig;
