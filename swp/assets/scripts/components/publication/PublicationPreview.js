import {useCallback, useMemo, useState} from 'react';
import classNames from 'classnames';
import PropTypes from 'prop-types';
import {Button, ButtonGroup} from '@blueprintjs/core';
import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';

import PublicationList from './PublicationList';


const Loading = _('Loading');
const NoPublications = _('No publications');
const PublicationsLabel = _('%s Publications');

const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);
const generatePageNumbers = count => Array(count).fill(0).map((e, i) => i + 1);


const PageButton = ({page, setCurrentPage, ...props}) => {
    const handleClick = useCallback(() => setCurrentPage(page), [page, setCurrentPage]);
    return (
        <Button onClick={handleClick} {...props}>
            {page}
        </Button>
    );
};

const PageButtons = ({pages, currentPage, setCurrentPage}) => pages.map(page => (
    <PageButton key={page} page={page} setCurrentPage={setCurrentPage} active={page === currentPage} />
));

const PublicationResults = ({publications, pageCount, currentPage, setCurrentPage, nextPage, prevPage, ...props}) => {
    const pages = useMemo(() => generatePageNumbers(pageCount), [pageCount]);

    const setNextPage = () => nextPage && setCurrentPage(currentPage + 1);
    const setPrevPage = () => prevPage && setCurrentPage(currentPage - 1);

    const handleNextPage = useCallback(setNextPage, [currentPage, setCurrentPage, nextPage]);
    const handlePrevPage = useCallback(setPrevPage, [currentPage, setCurrentPage, prevPage]);
    const handleFirstPage = useCallback(() => setCurrentPage(1), [setCurrentPage]);
    const handleLastPage = useCallback(() => setCurrentPage(pageCount), [setCurrentPage, pageCount]);

    return (
        <div className="publication-results">
            <PublicationList items={publications} {...props} />

            <div className="pagination mt-4" key="pagination">
                <ButtonGroup className="page-buttons">
                    <Button key="first" onClick={handleFirstPage} disabled={!prevPage} icon="double-chevron-left" />
                    <Button key="prev" onClick={handlePrevPage} disabled={!prevPage} icon="chevron-left" />
                    <PageButtons pages={pages} currentPage={currentPage} setCurrentPage={setCurrentPage} />
                    <Button key="next" onClick={handleNextPage} disabled={!nextPage} icon="chevron-right" />
                    <Button key="last" onClick={handleLastPage} disabled={!nextPage} icon="double-chevron-right" />
                </ButtonGroup>
            </div>
        </div>
    );
};


const PublicationPreview = ({thinktankID, page, pageSize, noTitle, className, ...props}) => {
    const [currentPage, setCurrentPage] = useState(page || 1);

    const endpoint = '/publication/';
    const params = {thinktank_id: thinktankID, page: currentPage, page_size: pageSize};
    const {loading, result} = useQuery(endpoint, params);

    if (loading) return Loading;

    const {data: {results: publications, next: nextPage, previous: prevPage, count}} = result;
    const title = count ? interpolate(PublicationsLabel, [count], false) : NoPublications;

    return (
        <div className={classNames('publication-preview', 'my-4', className)} {...props}>
            {noTitle || <header className="mb-2"><h3>{title}</h3></header>}

            <PublicationResults
                publications={publications}
                pageCount={calculatePageCount(count, pageSize)}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
                nextPage={nextPage}
                prevPage={prevPage}
            />
        </div>
    );
};

PublicationPreview.defaultProps = {
    page: 1,
    pageSize: 2,
    noTitle: false,
};

PublicationPreview.propTypes = {
    thinktankID: PropTypes.number.isRequired,
    page: PropTypes.number,
    pageSize: PropTypes.number,
    noTitle: PropTypes.bool,
};

export default PublicationPreview;
