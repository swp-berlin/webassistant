import {useMemo} from 'react';

import _, {interpolate} from 'utils/i18n';

import {useBreadcrumb} from 'components/Navigation';

import PoolQuery from './PoolQuery';

const EmptyPoolBreadcrumbText = _('Pool');
const AllPoolsBreadcrumbText = _('All Pools');
const FallbackPoolBreadcrumbText = _('Pool %s');
const DefaultPoolBreadcrumbText = _('Pool %(name)s (#%(id)s)');

const getPoolBreadcrumbText = data => {
    if (typeof data === 'number') return <PoolQueryBreadcrumb id={data} />;
    if (!data) return EmptyPoolBreadcrumbText;
    if (data === 'all') return AllPoolsBreadcrumbText;
    if ('pool' in data) return getPoolBreadcrumbText(data.pool);
    if ('thinktank' in data) return getPoolBreadcrumbText(data.thinktank);

    return interpolate(DefaultPoolBreadcrumbText, data);
};

const PoolQueryBreadcrumb = ({id}) => {
    const Loading = useMemo(
        () => {
            const Loading = () => interpolate(FallbackPoolBreadcrumbText, [id], false);

            Loading.displayName = `Pool ${id}(Loading)`;

            return Loading;
        },
        [id],
    );

    return (
        <PoolQuery id={id} components={{loading: Loading}}>
            {pool => getPoolBreadcrumbText(pool)}
        </PoolQuery>
    );
};

export const usePoolBreadcrumb = data => {
    const text = getPoolBreadcrumbText(data);

    return useBreadcrumb(null, text);
};
