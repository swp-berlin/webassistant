import _ from 'utils/i18n';

import SelectorResolverForm from './SelectorResolverForm';

const Label = _('Full-text');

const EmbeddingsResolverForm = props => <SelectorResolverForm {...props} label={Label} type="Embeddings" />;

export default EmbeddingsResolverForm;
