import {useEffect, useState} from 'react';
import {useBreadcrumb} from 'components/Navigation';
import Page from 'components/Page';
import ScraperTable from 'components/scraper/ScraperTable';

import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';
import ActivationButton from '../buttons/ActivationButton';


const UniqueLabel = _('Unique on');
const Nbsp = () => '\u00A0';


const ThinktankDetail = ({id, ...props}) => {
    const endpoint = `/thinktank/${id}/`;
    const {loading, result} = useQuery(endpoint);
    const [isActive, setActive] = useState(false);

    const label = loading ? interpolate('Thinktank %s', [id], false) : result.data.name;
    useBreadcrumb(endpoint, label);

    useEffect(() => {
        if (!loading) {
            setActive(result.data.is_active);
        }
    }, [loading]);

    if (loading) return 'Loading';

    const {data: thinktank} = result;
    const {
        unique_field: uniqueField,
        last_run: lastRun,
    } = thinktank;

    const onToggle = flag => setActive(flag);

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
        <Page title={label} actions={actions}>
            <div>
                {UniqueLabel}
                <Nbsp />
                <strong>{uniqueField}</strong>
            </div>

            <ScraperTable endpoint={`/thinktank/${id}/scrapers/`} {...props} />
        </Page>
    );
};

export default ThinktankDetail;
