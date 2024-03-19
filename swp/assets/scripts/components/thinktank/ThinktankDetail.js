import {Link, useParams} from 'react-router-dom';
import {useQuery} from 'react-query';

import _ from 'utils/i18n';

import {QueryResult} from 'components/Query';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import ScraperTable from 'components/scraper/ScraperTable';
import {getPublicationsLabel} from 'components/publication/helper';
import TableActions from 'components/tables/TableActions';

import ThinktankActivationButton from './ThinktankActivationButton';
import {useThinktanksBreadcrumb} from './ThinktankList';
import {getThinktankLabel} from './helper';

const EditLabel = _('Edit');
const NewScraperLabel = _('New scraper');
const UniqueLabel = _('Unique on');

const Nbsp = '\u00A0';


const ThinktankEditButton = ({id, ...props}) => (
    <Link to={`/thinktank/${id}/edit/`} className="bp3-button bp3-icon-edit" {...props}>
        {EditLabel}
    </Link>
);

const ScraperAddButton = ({id, ...props}) => (
    <Link to={`/thinktank/${id}/scraper/add/`} className="bp3-button bp3-icon-add" {...props}>
        {NewScraperLabel}
    </Link>
);

const UniqueFields = ({values}) => (
    <span>
        {UniqueLabel}
        {Nbsp}
        <strong>
            {values.join(' ')}
        </strong>
    </span>
);

const ThinktankDetail = props => {
    const {id} = useParams();
    const endpoint = `/thinktank/${id}/`;
    const query = useQuery(['thinktank', id]);
    const {data: thinktank, isLoading: loading} = query;
    const label = getThinktankLabel(id, {result: {data: thinktank}, loading});

    useThinktanksBreadcrumb();
    useBreadcrumb(endpoint, label);

    return (
        <QueryResult query={query}>
            {thinktank => {
                const {
                    description,
                    scrapers,
                    is_active: isActive,
                    can_manage: canManage,
                    unique_fields: uniqueFields,
                    publication_count: publicationCount,
                } = thinktank;

                const subtitle = <UniqueFields values={uniqueFields} />;

                const actions = canManage && (
                    <ThinktankActivationButton
                        id={id}
                        endpoint={endpoint}
                        isActive={isActive}
                        disabled={loading}
                    />
                );

                return (
                    <Page title={label} subtitle={subtitle} actions={actions}>
                        <Link to={`/thinktank/${id}/publications/`}>
                            {getPublicationsLabel(publicationCount)}
                        </Link>

                        <div className="flex justify-between items-end">
                            <p className="my-5 w-1/2">
                                {description}
                            </p>

                            {canManage && (
                                <TableActions>
                                    <ThinktankEditButton id={id} />
                                    <ScraperAddButton id={id} />
                                </TableActions>
                            )}
                        </div>

                        <ScraperTable {...props} items={scrapers} canManage={canManage} />
                    </Page>
                );
            }}
        </QueryResult>
    );
};

export default ThinktankDetail;
