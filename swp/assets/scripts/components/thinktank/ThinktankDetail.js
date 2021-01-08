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

    const label = loading ? interpolate('Thinktank %s', [id], false) : result.data.name;
    useBreadcrumb(endpoint, label);

    if (loading) return 'Loading';

    const {data: thinktank} = result;
    const {
        unique_field: uniqueField,
        last_run: lastRun,
        is_active: isActive,
    } = thinktank;

    const actions = [
        <ActivationButton key="isActive" endpoint={endpoint} isActive={isActive} />,
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
