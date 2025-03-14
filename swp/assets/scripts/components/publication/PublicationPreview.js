import {useLocation} from 'react-router-dom';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import _ from 'utils/i18n';

import {Query} from 'components/Fetch';
import {getPublicationsLabel, parsePageParam} from './helper';
import DownloadButton from './DownloadButton';
import PublicationResults from './PublicationResults';


const NoPublications = _('No publications');

const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);

const PublicationPreview = ({
    thinktankFilterID,
    thinktankID,
    monitorID,
    endpoint,
    params,
    since,
    isActive,
    page,
    pageSize,
    noTitle,
    className,
    downloadURL,
    categories,
    tags,
    onSelectTag,
    ...props
}) => {
    const location = useLocation();
    const currentPage = page || parsePageParam(location.search) || 1;

    const additionalParams = {page: currentPage, page_size: pageSize};
    if (thinktankFilterID) additionalParams.thinktankfilter = thinktankFilterID;
    if (thinktankID) additionalParams.thinktank_id = thinktankID;
    if (monitorID) additionalParams.monitor = monitorID;
    if (since) additionalParams.since = since;
    if (isActive !== null) additionalParams.is_active = isActive;

    return (
        <Query endpoint={endpoint} params={{...additionalParams, ...params}}>
            {({results, next: nextPage, previous: prevPage, count}) => (
                <div className={classNames('publication-preview', 'my-4', className)} {...props}>
                    {noTitle || (
                        <header className="flex space-x-4 mb-2">
                            <h3>{count ? getPublicationsLabel(count) : NoPublications}</h3>
                            {count > 0 && downloadURL && <DownloadButton href={downloadURL} />}
                        </header>
                    )}

                    {count > 0 && (
                        <PublicationResults
                            results={results}
                            pageCount={calculatePageCount(count, pageSize)}
                            currentPage={currentPage}
                            nextPage={nextPage}
                            prevPage={prevPage}
                        />
                    )}
                </div>
            )}
        </Query>
    );
};

PublicationPreview.defaultProps = {
    thinktankFilterID: null,
    thinktankID: null,
    monitorID: null,
    endpoint: '/publication/',
    since: null,
    isActive: null,
    page: null,
    pageSize: 10,
    noTitle: false,
    downloadURL: '',
};

PublicationPreview.propTypes = {
    thinktankFilterID: PropTypes.number,
    thinktankID: PropTypes.number,
    monitorID: PropTypes.number,
    endpoint: PropTypes.string,
    since: PropTypes.oneOfType([
        PropTypes.instanceOf(Date),
        PropTypes.string,
    ]),
    isActive: PropTypes.bool,
    page: PropTypes.number,
    pageSize: PropTypes.number,
    noTitle: PropTypes.bool,
    downloadURL: PropTypes.string,
};

export default PublicationPreview;
