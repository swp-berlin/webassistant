import PageHeading from './PageHeading';

const Page = ({children, className, ...props}) => (
    <>
        <main className={className}>
            <PageHeading {...props} />
            {children}
        </main>
        <div id="portal" />
    </>
);

export default Page;
