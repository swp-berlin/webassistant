const TagCloud = ({label, children}) => (
    <div className="mt-2 mb-4 flex flex-wrap space-x-2">
        <span>{label}</span>
        {children}
    </div>
);

export default TagCloud;
