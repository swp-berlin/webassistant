import _ from 'utils/i18n';

import PoolQuery from 'components/PoolQuery';

import TagCloud from './TagCloud';
import InteractiveTag from './InteractiveTag';

const Label = _('Filter by Pool:');

const PoolTagCloud = ({selected, onSelect}) => (
    <PoolQuery canManage>
        {pools => pools.length > 0 && (
            <TagCloud label={Label}>
                {pools.map(({id, name}) => (
                    <InteractiveTag
                        key={id}
                        value={id}
                        label={name}
                        selected={selected.includes(id)}
                        onClick={onSelect}
                    />
                ))}
            </TagCloud>
        )}
    </PoolQuery>
);

export default PoolTagCloud;
