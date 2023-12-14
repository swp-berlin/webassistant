import Portal from 'components/Portal';

const ContainerID = 'scraper-activation-container';

export const ScraperActivationPortal = ({children}) => (
    <Portal id={ContainerID}>
        {children}
    </Portal>
);

const ScraperActivationContainer = () => <div id={ContainerID} />;

export default ScraperActivationContainer;
