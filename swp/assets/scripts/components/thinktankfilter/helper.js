
export const getThinktankFilterPublicationsURL = (id, monitorID, onlyNew = false) => {
    const newPath = onlyNew ? 'new/' : '';
    return `/monitor/${monitorID}/filter/${id}/publications/${newPath}`;
};

export const getThinktankFilterDownloadURL = (id, monitorID, onlyNew = false) => {
    const newPath = onlyNew ? 'new/' : '';
    return `/monitor/${monitorID}/filter/${id}/publications/download/${newPath}`;
};
