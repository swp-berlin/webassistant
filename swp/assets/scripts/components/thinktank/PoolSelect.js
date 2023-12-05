import {useCallback, useState} from 'react';

import _ from 'utils/i18n';

import {ChoicesQuery} from 'components/Fetch';
import {Select} from 'components/forms';
import {getJSON, setJSON} from 'utils/localStorage';

const AllChoice = {
    value: null,
    label: _('All'),
};

const prepareChoice = ({id, name}) => ({value: id, label: name});

const prepareChoices = pools => [AllChoice, ...pools.map(prepareChoice)];

const PoolSelect = props => (
    <ChoicesQuery endpoint="pool" prepareChoices={prepareChoices}>
        <Select className="mb-0 mr-2" name="pool" {...props} />
    </ChoicesQuery>
);

const LocalStorageKey = 'last-selected-pool';

const getDefaultPool = () => getJSON(LocalStorageKey, AllChoice.value);

export const usePoolSelect = () => {
    const [pool, setPool] = useState(getDefaultPool);

    const handleChange = useCallback(
        pool => {
            setPool(pool);
            setJSON(LocalStorageKey, pool);
        },
        [setPool],
    );

    const poolSelect = <PoolSelect value={pool} onChange={handleChange} />;

    return [pool, poolSelect];
};
