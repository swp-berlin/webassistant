import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExternalLinkAlt} from '@fortawesome/free-solid-svg-icons/faExternalLinkAlt';


// TODO This should be implemented via stylesheet at some point
const ExternalLink = ({children, to, ...props}) => (
    <a href={to} rel="noreferrer" target="_blank" {...props}>
        {children || to}
        <FontAwesomeIcon className="ml-1" icon={faExternalLinkAlt} size="xs" />
    </a>
);

export default ExternalLink;
