import {useLocation} from 'react-router-dom';

function createSearchParams(init="") {
    return new URLSearchParams(
        typeof init === "string"
        || Array.isArray(init)
        || init instanceof URLSearchParams
            ? init : Object.keys(init).reduce((memo, key) => {
                let value = init[key];
                return memo.concat(
                    Array.isArray(value) ? value.map((v) => [key, v]) : [[key, value]]
                );
            }, [])
    );
}

function getSearchParamsForLocation(locationSearch, defaultSearchParams) {
    let searchParams = createSearchParams(locationSearch);

    for (let key of defaultSearchParams.keys()) {
        if (!searchParams.has(key)) {
            defaultSearchParams.getAll(key).forEach((value) => {
                searchParams.append(key, value);
            });
        }
    }

    return searchParams;
}

export function useSearchParams(defaultInit){
    let defaultSearchParamsRef = React.useRef(createSearchParams(defaultInit));

    let location = useLocation();
    let searchParams = React.useMemo(
        () => getSearchParamsForLocation(location.search, defaultSearchParamsRef.current),
        [location.search]
    );

    let navigate = useNavigate();
    let setSearchParams = React.useCallback<SetURLSearchParams>(
        (nextInit, navigateOptions) => {
            const newSearchParams = createSearchParams(
                typeof nextInit === "function" ? nextInit(searchParams) : nextInit
            );
            navigate("?" + newSearchParams, navigateOptions);
        },
            [navigate, searchParams]
    );

    return [searchParams, setSearchParams];
}
