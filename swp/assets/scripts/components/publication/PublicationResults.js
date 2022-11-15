import {useMemo} from 'react';
import {Link, useLocation} from 'react-router-dom';
import classNames from 'classnames';
import {ButtonGroup, Icon} from '@blueprintjs/core';

import {withPageParam} from './helper';
import PublicationList from './PublicationList';


const generatePageNumbers = count => Array(count).fill(0).map((e, i) => i + 1);

const PageButton = ({page, active, icon, disabled, ...props}) => {
    const location = useLocation();
    const to = {
        pathname: location.pathname,
        search: withPageParam(location.search, page),
    };

    return (
        <Link className={classNames('bp3-button', active && 'bp3-active', disabled && 'bp3-disabled')} to={to} disabled={disabled} {...props}>
            {icon ? <Icon icon={icon} /> : page}
        </Link>
    );
};

const PageButtons = ({pages, currentPage}) => pages.map(page => (
    <PageButton key={page} page={page} active={page === currentPage} />
));

const PublicationResults = ({results, pageCount, currentPage, nextPage, prevPage, ...props}) => {
    const pages = useMemo(() => generatePageNumbers(pageCount), [pageCount]);

    const nextPageNumber = Math.min(currentPage + 1, pageCount);
    const prevPageNumber = Math.max(currentPage - 1, 1);

    return (
        <div className="publication-results">
            <PublicationList items={results} {...props} showMenu />

            <div className="pagination mt-4" key="pagination">
                <ButtonGroup className="page-buttons">
                    <PageButton key="first" page={1} disabled={!prevPage} icon="double-chevron-left" />
                    <PageButton key="prev" page={prevPageNumber} disabled={!prevPage} icon="chevron-left" />
                    <PageButtons pages={pages} currentPage={currentPage} />
                    <PageButton key="next" page={nextPageNumber} disabled={!nextPage} icon="chevron-right" />
                    <PageButton key="last" page={pageCount} disabled={!nextPage} icon="double-chevron-right" />
                </ButtonGroup>
            </div>
        </div>
    );
};

export default PublicationResults;
