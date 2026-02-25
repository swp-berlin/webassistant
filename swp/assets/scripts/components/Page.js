import PageHeading from './PageHeading';
import {Fragment} from 'react';

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
