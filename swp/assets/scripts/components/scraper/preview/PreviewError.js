import {Callout} from '@blueprintjs/core';
import _ from 'utils/i18n';


const Title = _('Scraper Error');
const Description = _('Scraping failed with the following error:');


const PreviewError = ({error, title, description, ...props}) => (
    <Callout intent="danger" title={title} {...props}>
        <p>{description}</p>
        <pre className="mt-2 whitespace-pre-line">
            {error}
        </pre>
    </Callout>
);

PreviewError.defaultProps = {
    title: Title,
    description: Description,
};

export default PreviewError;
