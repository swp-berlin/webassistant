const PageHeading = ({title, subtitle, actions}) => (
    <div className="lg:flex lg:items-center lg:justify-between">
        <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
                {title}
            </h2>
            <div className="mt-1 flex flex-col sm:flex-row sm:flex-wrap sm:mt-0 sm:space-x-6">
                {subtitle}
            </div>
        </div>
        <div className="mt-5 flex lg:mt-0 lg:ml-4">
            {actions}
        </div>
    </div>
);

export default PageHeading;
