import {createContext, useContext} from 'react';


const ResolverFormContext = createContext(null);

export const useResolverForm = type => {
    const types = useContext(ResolverFormContext);

    return types[type];
};

export default ResolverFormContext.Provider;
