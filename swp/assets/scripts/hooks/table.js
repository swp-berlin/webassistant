import {useMemo} from 'react';

import {DefaultComponents} from 'components/Query/QueryResult';

export const getQueryComponents = (colSpan, components = DefaultComponents) => {
    const wrappedComponents = {};

    Object.entries(components).forEach(([key, Component]) => {
        const Wrapper = props => (
            <tr>
                <td colSpan={colSpan}>
                    <Component {...props} />
                </td>
            </tr>
        );

        Wrapper.displayName = `TableRowWrapper(${key})`;

        wrappedComponents[key] = Wrapper;
    });

    return wrappedComponents;
};

export const useQueryComponents = (colSpan, components = DefaultComponents) => useMemo(
    () => getQueryComponents(colSpan, components),
    [colSpan, components],
);
