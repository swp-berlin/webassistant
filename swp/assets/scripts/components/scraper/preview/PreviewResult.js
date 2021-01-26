import {Status} from './common';


// TODO replace with Component from https://cosmocode.jira.com/browse/SWP-47
const Publication = ({publication}) => (
    <pre>{JSON.stringify(publication, null, 2)}</pre>
);


const PreviewResult = ({status, publications, traceback}) => {
    if (status === Status.Failure) {
        return <pre>{traceback}</pre>;
    }

    return (
        <ul>
            {status === Status.Success && publications.map((publication, idx) => (
                // eslint-disable-next-line react/no-array-index-key
                <li key={idx}><Publication publication={publication} /></li>
            ))}
        </ul>
    );
};

export default PreviewResult;
