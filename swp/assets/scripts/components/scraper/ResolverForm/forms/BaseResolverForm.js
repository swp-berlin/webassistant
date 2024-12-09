const BaseResolverForm = ({label, children}) => (
    <div>
        <h2 className="text-lg mb-4">{label}</h2>
        {children}
    </div>
);

export default BaseResolverForm;
