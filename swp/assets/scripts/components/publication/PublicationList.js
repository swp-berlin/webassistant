import classNames from 'classnames';

import PublicationItem from './PublicationItem';

const getClassName = (items, className) => classNames(
    'publication-list',
    'list-none',
    'space-y-4',
    'p-0',
    className,
    {empty: items.length === 0},
);

const PublicationList = ({items, className, onAddFilter, children, ...props}) => (
    <ul className={getClassName(items, className)} {...props}>
        {items.map(publication => (
            <li key={publication.id}>
                <PublicationItem publication={publication} onAddFilter={onAddFilter}>
                    {children}
                </PublicationItem>
            </li>
        ))}
    </ul>
);

export default PublicationList;
