import RemoteSnippet from 'components/RemoteSnippet';


const ScraperTypeDescription = ({form: {watch}}) => {
    const type = watch('type');

    return <RemoteSnippet className="w-3/6" identifier={`scraper-type/${type}`} />;
};

export default ScraperTypeDescription;
