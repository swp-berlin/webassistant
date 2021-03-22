import {useCallback, useEffect, useState} from 'react';
import {Link} from 'react-router-dom';

import ActivationButton from 'components/buttons/ActivationButton';
import {Result} from 'components/Fetch';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import ScraperTable from 'components/scraper/ScraperTable';
import {getPublicationsLabel} from 'components/publication/helper';
import TableActions from 'components/tables/TableActions';

import {useQuery} from 'hooks/query';
import _ from 'utils/i18n';
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

const ThinktankDetail = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const result = useQuery(endpoint);
    const [isActive, setActive] = useState(false);
    const {loading, result: {data: thinktank}, success} = result;

    const label = getThinktankLabel(id, result);
    useThinktanksBreadcrumb();
    useBreadcrumb(endpoint, label);

    const onToggle = useCallback(
        flag => setActive(flag),
        [setActive],
    );

    useEffect(() => {
        if (success) {
            setActive(thinktank.is_active);
        }
    }, [success, thinktank]);

    const actions = [
        <ActivationButton
            key="isActive"
            endpoint={endpoint}
            isActive={isActive}
            onToggle={onToggle}
            disabled={loading}
        />,
    ];

    return (
        <Result result={result}>
            {({description, unique_fields: uniqueFields, publication_count: publicationCount, scrapers}) => (
                <Page title={label} subtitle={<UniqueFields values={uniqueFields} />} actions={actions}>
                    <Link to={`/thinktank/${id}/publications/`}>
                        {getPublicationsLabel(publicationCount)}
                    </Link>

                    <div className="flex justify-between items-end">
                        <p className="my-5 w-1/2">
                            {description}
                        </p>

                        <TableActions>
                            <ThinktankEditButton id={id} />
                            <ScraperAddButton id={id} />
                        </TableActions>
                    </div>

                    <ScraperTable items={scrapers} {...props} />
                </Page>
            )}
        </Result>
    );
};

export default ThinktankDetail;
