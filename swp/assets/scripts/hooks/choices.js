import {useMemo} from 'react';

import {translated, getLabel} from 'utils/choices';

export const useTranslated = name => useMemo(() => translated(name), [name]);

export const useLabel = (name, value) => useMemo(() => getLabel(name, value), [name, value]);
