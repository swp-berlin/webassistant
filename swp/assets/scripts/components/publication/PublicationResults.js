import {useCallback, useMemo} from 'react';
import {Link, useLocation} from 'react-router-dom';
import classNames from 'classnames';
import {ButtonGroup, Icon} from '@blueprintjs/core';

import PublicationList from './PublicationList';


const generatePageNumbers = count => Array(count).fill(0).map((e, i) => i + 1);

const PageButton = ({page, setCurrentPage, onClick, active, icon, disabled, ...props}) => {
    const location = useLocation();
    const search = new URLSearchParams(location.search);
    search.set('page', page);
    const to = {
        pathname: location.pathname,
        search: search.toString(),
    };

    const handleClick = useCallback(() => setCurrentPage(page), [page, setCurrentPage]);

    return (
        <Link className={classNames('bp3-button', active && 'bp3-active', disabled && 'bp3-disabled')} to={to} onClick={onClick || handleClick} disabled={disabled} {...props}>
            {icon ? <Icon icon={icon} /> : page}
        </Link>
    );
};

const PageButtons = ({pages, currentPage, setCurrentPage}) => pages.map(page => (
    <PageButton key={page} page={page} setCurrentPage={setCurrentPage} active={page === currentPage} />
));

const PublicationResults = ({results, pageCount, currentPage, setCurrentPage, nextPage, prevPage, ...props}) => {
    const pages = useMemo(() => generatePageNumbers(pageCount), [pageCount]);

    const nextPageNumber = Math.min(currentPage + 1, pageCount);
    const prevPageNumber = Math.max(currentPage - 1, 1);

    const handleNextPage = useCallback(() => nextPage && setCurrentPage(page => page + 1), [setCurrentPage, nextPage]);
    const handlePrevPage = useCallback(() => prevPage && setCurrentPage(page => page - 1), [setCurrentPage, prevPage]);
    const handleFirstPage = useCallback(() => setCurrentPage(1), [setCurrentPage]);
    const handleLastPage = useCallback(() => setCurrentPage(pageCount), [setCurrentPage, pageCount]);

    return (
        <div className="publication-results">
            <PublicationList items={results} {...props} />

            <div className="pagination mt-4" key="pagination">
                <ButtonGroup className="page-buttons">
                    <PageButton key="first" page={1} disabled={!prevPage} onClick={handleFirstPage} icon="double-chevron-left" />
                    <PageButton key="prev" page={prevPageNumber} onClick={handlePrevPage} disabled={!prevPage} icon="chevron-left" />
                    <PageButtons pages={pages} currentPage={currentPage} setCurrentPage={setCurrentPage} />
                    <PageButton key="next" page={nextPageNumber} onClick={handleNextPage} disabled={!nextPage} icon="chevron-right" />
                    <PageButton key="last" page={pageCount} onClick={handleLastPage} disabled={!nextPage} icon="double-chevron-right" />
                </ButtonGroup>
            </div>
        </div>
    );
};

export default PublicationResults;
