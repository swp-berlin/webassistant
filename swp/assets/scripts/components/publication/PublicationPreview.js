import {useState} from 'react';
import PropTypes from 'prop-types';
import {Button, ButtonGroup} from '@blueprintjs/core';
import {useQuery} from 'hooks/query';
import _, {interpolate} from 'utils/i18n';

import PublicationList from './PublicationList';


const Loading = _('Loading');
const NoPublications = _('No publications');

const calculatePageCount = (total, pageSize) => Math.ceil(total / pageSize);
const generatePageNumbers = (total, pageSize) => Array(calculatePageCount(total, pageSize)).fill().map((e, i) => i + 1);


const PublicationPreview = ({thinktankID, page, pageSize, ...props}) => {
    const [currentPage, setCurrentPage] = useState(page || 1);

    const endpoint = '/publication/';
    const {loading, result} = useQuery(endpoint, {thinktank_id: thinktankID, page: currentPage, page_size: pageSize});

    if (loading) return Loading;
    const {results: publications, next: nextPage, previous: prevPage, count: total} = result.data;

    const pages = generatePageNumbers(total, pageSize);

    const handleNextPage = () => (nextPage && setCurrentPage(currentPage + 1));
    const handlePrevPage = () => (prevPage && setCurrentPage(currentPage - 1));

    const title = interpolate('%s Publications', [total], false);

    return (
        <div className="publication-preview" {...props}>
            <header className="mb-4">
                <h3>{title || NoPublications}</h3>
            </header>

            <PublicationList items={publications} />

            <div className="pagination mt-4" key="pagination">
                <ButtonGroup className="page-buttons">
                    <Button key="prev" onClick={handlePrevPage} disabled={!prevPage} icon="double-chevron-left" />
                    {pages.map(page => (
                        <Button key={page} onClick={() => setCurrentPage(page)} active={page === currentPage}>
                            {page}
                        </Button>
                    ))}
                    <Button key="next" onClick={handleNextPage} disabled={!nextPage} icon="double-chevron-right" />
                </ButtonGroup>
            </div>
        </div>
    );
};

PublicationPreview.defaultProps = {
    page: 1,
    pageSize: 2,
};

PublicationPreview.propTypes = {
    thinktankID: PropTypes.number.isRequired,
    page: PropTypes.number,
    pageSize: PropTypes.number,
};

export default PublicationPreview;
