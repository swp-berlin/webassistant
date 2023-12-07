import Query from 'components/Query';

import _ from 'utils/i18n';

import TagCloud from './TagCloud';
import InteractiveTag from './InteractiveTag';

const Endpoint = 'pool';
const Params = {can_manage: true};
const QueryKey = [Endpoint, Params];

const Label = _('Filter by Pool:');

const PoolTagCloud = ({selected, onSelect}) => (
    <Query queryKey={QueryKey}>
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
    </Query>
);

export default PoolTagCloud;
