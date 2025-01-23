import PublicationResults from 'components/publication/PublicationResults';
import {calculatePageCount} from 'components/Search/SearchResult';
import SearchResultHeader from 'components/Search/SearchResultHeader';

const MonitorQueryResult = ({results, count = 0, page: currentPage, next: nextPage, previous: prevPage}) => {
    const pageCount = calculatePageCount(count, 10);

    return (
        <div className="publication-preview my-4">
            <SearchResultHeader count={count} query="" />
            {count > 0 && (
                <PublicationResults
                    currentPage={currentPage || 1}
                    nextPage={nextPage}
                    prevPage={prevPage}
                    pageCount={pageCount}
                    results={results}
                />
            )}
        </div>
    );
};

export default MonitorQueryResult;
