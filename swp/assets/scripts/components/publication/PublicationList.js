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

const PublicationList = ({items, className, showMenu, ...props}) => (
    <ul className={getClassName(items, className)} {...props}>
        {items.map(publication => (
            <li key={publication.id}>
                <PublicationItem publication={publication} showMenu={showMenu} />
            </li>
        ))}
    </ul>
);

export default PublicationList;
