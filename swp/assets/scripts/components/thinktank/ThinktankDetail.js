import {useCallback, useEffect, useState} from 'react';
import {Link} from 'react-router-dom';

import ActivationButton from 'components/buttons/ActivationButton';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import PublicationPreview from 'components/publication/PublicationPreview';
import ScraperTable from 'components/scraper/ScraperTable';
import TableActions from 'components/tables/TableActions';

import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';
import {useThinktanksBreadcrumb} from './ThinktankList';

const Loading = _('Loading');
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

const ThinktankDetail = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const {loading, result: {data: thinktank}, success} = useQuery(endpoint);
    const [isActive, setActive] = useState(false);

    useThinktanksBreadcrumb();
    const label = loading ? interpolate('Thinktank %s', [id], false) : thinktank.name;
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

    if (loading) return Loading;

    const {
        description,
        unique_field: uniqueField,
        scrapers,
    } = thinktank;

    const actions = [
        <ActivationButton
            key="isActive"
            endpoint={endpoint}
            isActive={isActive}
            onToggle={onToggle}
            disabled={loading}
        />,
    ];

    const subtitle = (
        <span>
            {UniqueLabel}
            {Nbsp}
            <strong>{uniqueField}</strong>
        </span>
    );

    return (
        <Page title={label} subtitle={subtitle} actions={actions}>
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

            <PublicationPreview thinktankID={id} />
        </Page>
    );
};

export default ThinktankDetail;
