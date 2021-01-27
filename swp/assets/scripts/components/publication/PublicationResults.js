import {useCallback, useMemo} from 'react';
import {Button, ButtonGroup} from '@blueprintjs/core';

import PublicationList from './PublicationList';


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

const PublicationResults = ({results, pageCount, currentPage, setCurrentPage, nextPage, prevPage, ...props}) => {
    const pages = useMemo(() => generatePageNumbers(pageCount), [pageCount]);

    const setNextPage = () => nextPage && setCurrentPage(currentPage + 1);
    const setPrevPage = () => prevPage && setCurrentPage(currentPage - 1);

    const handleNextPage = useCallback(setNextPage, [currentPage, setCurrentPage, nextPage]);
    const handlePrevPage = useCallback(setPrevPage, [currentPage, setCurrentPage, prevPage]);
    const handleFirstPage = useCallback(() => setCurrentPage(1), [setCurrentPage]);
    const handleLastPage = useCallback(() => setCurrentPage(pageCount), [setCurrentPage, pageCount]);

    return (
        <div className="publication-results">
            <PublicationList items={results} {...props} />

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

export default PublicationResults;
