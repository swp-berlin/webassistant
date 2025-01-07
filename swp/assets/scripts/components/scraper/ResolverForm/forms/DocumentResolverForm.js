import _ from 'utils/i18n';

import SelectorResolverForm from './SelectorResolverForm';

const Label = _('Document');

const DocumentResolverForm = props => <SelectorResolverForm {...props} label={Label} type="Document" />;

export default DocumentResolverForm;
