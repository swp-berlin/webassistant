import RemoteSnippet from 'components/RemoteSnippet';


const ScraperTypeDescription = ({form: {watch}}) => {
    const type = watch('type');

    return <RemoteSnippet identifier={`scraper-type/${type}`} />;
};

export default ScraperTypeDescription;
