import {useEffect, useState} from 'react';
import {useLocation} from 'react-router-dom';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import {useQuery} from 'hooks/query';
import _ from 'utils/i18n';

import {getPublicationsLabel} from './helper';
import PublicationResults from './PublicationResults';


const Loading = _('Loading');
const NoPublications = _('No publications');

const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);

const PublicationPreview = ({thinktankID, page, pageSize, noTitle, className, ...props}) => {
    const location = useLocation();
    const [currentPage, setCurrentPage] = useState(page || 1);

    useEffect(
        () => {
            const params = new URLSearchParams(location.search);
            const pageParam = +params.get('page');

            if (pageParam && pageParam !== currentPage) {
                setCurrentPage(pageParam);
            }
        },
        [location, currentPage, setCurrentPage],
    );

    const endpoint = '/publication/';
    const params = {thinktank_id: thinktankID, page: currentPage, page_size: pageSize};
    const {loading, result} = useQuery(endpoint, params);

    if (loading) return Loading;

    const {data: {results, next: nextPage, previous: prevPage, count}} = result;
    const title = count ? getPublicationsLabel(count) : NoPublications;

    return (
        <div className={classNames('publication-preview', 'my-4', className)} {...props}>
            {noTitle || <header className="mb-2"><h3>{title}</h3></header>}

            {count > 0 && (
                <PublicationResults
                    results={results}
                    pageCount={calculatePageCount(count, pageSize)}
                    currentPage={currentPage}
                    setCurrentPage={setCurrentPage}
                    nextPage={nextPage}
                    prevPage={prevPage}
                />
            )}
        </div>
    );
};

PublicationPreview.defaultProps = {
    page: null,
    pageSize: 10,
    noTitle: false,
};

PublicationPreview.propTypes = {
    thinktankID: PropTypes.number.isRequired,
    page: PropTypes.number,
    pageSize: PropTypes.number,
    noTitle: PropTypes.bool,
};

export default PublicationPreview;
