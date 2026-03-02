import {Fragment} from 'react';
import PageHeading from './PageHeading';

const Page = ({children, className, ...props}) => (
    <Fragment>
        <main className={className}>
            <PageHeading {...props} />
            {children}
        </main>
        <div id="portal" />
    </Fragment>
);

export default Page;
