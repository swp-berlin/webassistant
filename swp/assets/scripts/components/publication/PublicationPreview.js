import {useState} from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import {Button, ButtonGroup} from '@blueprintjs/core';
import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';

import PublicationList from './PublicationList';


const Loading = _('Loading');
const NoPublications = _('No publications');

const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);
const generatePageNumbers = (total, pageSize) => Array(calculatePageCount(total, pageSize)).fill().map((e, i) => i + 1);


const PublicationPreview = ({thinktankID, page, pageSize, noTitle, className, ...props}) => {
    const [currentPage, setCurrentPage] = useState(page || 1);

    const endpoint = '/publication/';
    const {loading, result} = useQuery(endpoint, {thinktank_id: thinktankID, page: currentPage, page_size: pageSize});

    if (loading) return Loading;
    const {results: publications, next: nextPage, previous: prevPage, count} = result.data;

    const pages = generatePageNumbers(count, pageSize);

    const handleNextPage = () => (nextPage && setCurrentPage(currentPage + 1));
    const handlePrevPage = () => (prevPage && setCurrentPage(currentPage - 1));
    const handleFirstPage = () => setCurrentPage(1);
    const handleLastPage = () => setCurrentPage(pages.length);

    const title = count ? interpolate(_('%s Publications'), [count], false) : NoPublications;

    return (
        <div className={classNames('publication-preview', 'my-4', className)} {...props}>
            {noTitle || <header className="mb-2"><h3>{title}</h3></header>}

            <PublicationList items={publications} />

            <div className="pagination mt-4" key="pagination">
                <ButtonGroup className="page-buttons">
                    <Button key="first" onClick={handleFirstPage} disabled={!prevPage} icon="double-chevron-left" />
                    <Button key="prev" onClick={handlePrevPage} disabled={!prevPage} icon="chevron-left" />
                    {pages.map(page => (
                        <Button key={page} onClick={() => setCurrentPage(page)} active={page === currentPage}>
                            {page}
                        </Button>
                    ))}
                    <Button key="next" onClick={handleNextPage} disabled={!nextPage} icon="chevron-right" />
                    <Button key="last" onClick={handleLastPage} disabled={!nextPage} icon="double-chevron-right" />
                </ButtonGroup>
            </div>
        </div>
    );
};

PublicationPreview.defaultProps = {
    page: 1,
    pageSize: 3,
    noTitle: false,
};

PublicationPreview.propTypes = {
    thinktankID: PropTypes.number.isRequired,
    page: PropTypes.number,
    pageSize: PropTypes.number,
    noTitle: PropTypes.bool,
};

export default PublicationPreview;
