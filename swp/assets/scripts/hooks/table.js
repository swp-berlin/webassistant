import {useMemo} from 'react';
import {
    handleLoading,
} from 'components/Fetch/defaultHandler';


export const useFetchHandler = colSpan => useMemo(
    () => {
        const wrap = handler => (...args) => (
            <tr>
                <td colSpan={colSpan}>
                    {handler(...args)}
                </td>
            </tr>
        );

        return {
            handleLoading: wrap(handleLoading),
        };
    },
    [colSpan],
);
