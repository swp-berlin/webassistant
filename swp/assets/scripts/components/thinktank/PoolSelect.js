import {useCallback, useState} from 'react';

import _ from 'utils/i18n';
import {getJSON, setJSON} from 'utils/localStorage';

import {ChoicesQuery} from 'components/Fetch';
import {Select} from 'components/forms';

const AllChoice = {
    id: null,
    name: _('All'),
    can_manage: false,
};

const prepareChoice = ({id, name, can_manage: canManage}) => ({
    value: id,
    label: name,
    icon: canManage ? 'edit' : 'eye-open',
});

const prepareChoices = pools => {
    const canManage = pools.every(({can_manage: canManage}) => canManage);

    return [
        prepareChoice({...AllChoice, can_manage: canManage}),
        ...pools.map(prepareChoice),
    ];
};

const PoolSelect = props => (
    <ChoicesQuery endpoint="pool" prepareChoices={prepareChoices}>
        <Select className="mb-0 mr-2" name="pool" {...props} />
    </ChoicesQuery>
);

const LocalStorageKey = 'last-selected-pool';

const getDefaultPool = () => getJSON(LocalStorageKey, AllChoice.id);

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
