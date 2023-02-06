import {Tag} from '@blueprintjs/core';

import _ from 'utils/i18n';

const Label = _('Default');

const DefaultTag = ({label = Label}) => (<Tag className="ml-1">{label}</Tag>);

export default DefaultTag;
