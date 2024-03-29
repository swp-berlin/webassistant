import {createContext, useContext, useEffect, useRef} from 'react';
import {Link} from 'react-router-dom';

import {Breadcrumb, Breadcrumbs as BlueprintBreadcrumbs} from '@blueprintjs/core';


export const BreadcrumbContext = createContext(null);

export const useBreadcrumb = (href, text, icon = null) => {
    const addBreadcrumb = useContext(BreadcrumbContext);
    const changeBreadcrumbRef = useRef(null);

    useEffect(
        () => {
            const {changeBreadcrumb, removeBreadcrumb} = addBreadcrumb({href, text, icon});
            changeBreadcrumbRef.current = changeBreadcrumb;

            return removeBreadcrumb;
        },
        // eslint-disable-next-line react-hooks/exhaustive-deps
        [addBreadcrumb],
    );

    useEffect(
        () => {
            changeBreadcrumbRef.current({href, text, icon});
        },
        [href, text, icon, changeBreadcrumbRef],
    );
};

const BreadcrumbRenderer = ({href, ...props}) => {
    const breadcrumb = <Breadcrumb {...props} />;

    if (href === null) return breadcrumb;

    return (
        <Link to={href}>
            {breadcrumb}
        </Link>
    );
};

const CurrentBreadcrumbRenderer = props => <BreadcrumbRenderer {...props} current />;

const Breadcrumbs = props => (
    <BlueprintBreadcrumbs
        {...props}
        breadcrumbRenderer={BreadcrumbRenderer}
        currentBreadcrumbRenderer={CurrentBreadcrumbRenderer}
    />
);

export default Breadcrumbs;
