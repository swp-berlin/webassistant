import {useLocation} from 'react-router-dom';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import _ from 'utils/i18n';

import {Query} from 'components/Fetch';
import {getPublicationsLabel, parsePageParam} from './helper';
import PublicationResults from './PublicationResults';


const NoPublications = _('No publications');

const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);

const PublicationPreview = ({thinktankID, endpoint, page, pageSize, noTitle, className, ...props}) => {
    const location = useLocation();
    const currentPage = page || parsePageParam(location.search) || 1;

    const params = {thinktank_id: thinktankID, page: currentPage, page_size: pageSize};

    return (
        <Query endpoint={endpoint} params={params}>
            {({results, next: nextPage, previous: prevPage, count}) => (
                <div className={classNames('publication-preview', 'my-4', className)} {...props}>
                    {noTitle || (
                        <header className="mb-2">
                            <h3>{count ? getPublicationsLabel(count) : NoPublications}</h3>
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
    endpoint: '/publication/',
    page: null,
    pageSize: 3,
    noTitle: false,
};

PublicationPreview.propTypes = {
    thinktankID: PropTypes.number.isRequired,
    endpoint: PropTypes.string,
    page: PropTypes.number,
    pageSize: PropTypes.number,
    noTitle: PropTypes.bool,
};

export default PublicationPreview;
