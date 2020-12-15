import {NonIdealState, Spinner} from '@blueprintjs/core';

import _ from 'utils/i18n';

const Title = _('Loading…');
const Description = _('Please wait, we are loading your content.');

const Loading = props => (
    <NonIdealState {...props} />
);

Loading.defaultProps = {
    icon: (<Spinner />),
    title: Title,
    description: Description,
};

export default Loading;
