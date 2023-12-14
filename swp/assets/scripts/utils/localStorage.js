export const getItem = key => {
    try {
        if (window.localStorage) return window.localStorage.getItem(key);
    } catch (error) {
        return undefined;
    }
};

export const setItem = (key, value) => {
    try {
        if (window.localStorage) return window.localStorage.setItem(key, value);
    } catch (error) {
        return error;
    }
};

export const getJSON = (key, defaultValue = null) => {
    const value = getItem(key);

    if (!value) return defaultValue;

    try {
        return JSON.parse(value);
    } catch (error) {
        return defaultValue;
    }
};

export const setJSON = (key, value) => setItem(key, JSON.stringify(value));
