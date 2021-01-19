import ReactMarkdown from 'react-markdown';

/* a fix for VFile */
window.process = {
    cwd: () => '',
};

export default ReactMarkdown;
