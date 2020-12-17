import {useCallback, useState} from 'react';

import _ from 'utils/i18n';
import {BreadcrumbContext} from './Breadcrumbs';
import Navbar from './Navbar';


const HomeBreadcrumb = {
    href: '/',
    text: _('Home'),
    icon: 'home',
};

const Navigation = ({children}) => {
    const [breadcrumbs, setBreadcrumbs] = useState([HomeBreadcrumb]);

    const addCallback = data => {
        let breadcrumb = data;

        const changeBreadcrumb = data => {
            setBreadcrumbs(items => items.map(current => {
                if (current === breadcrumb) {
                    breadcrumb = data;

                    return breadcrumb;
                }

                return current;
            }));
        };

        const removeBreadcrumb = () => {
            setBreadcrumbs(items => items.filter(current => current !== breadcrumb));
        };

        setBreadcrumbs(items => [...items, breadcrumb]);
        return {changeBreadcrumb, removeBreadcrumb};
    };

    const addBreadcrumb = useCallback(addCallback, [setBreadcrumbs]);

    return (
        <BreadcrumbContext.Provider value={addBreadcrumb}>
            <Navbar breadcrumbs={breadcrumbs} />
            {children}
        </BreadcrumbContext.Provider>
    );
};

export default Navigation;
export * from './Breadcrumbs';
