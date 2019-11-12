export
const loggedIn = () => {
    return (window as any).user;
};

export
const basepath = () => {
    return (window as any).CONNECTION_CONFIG.basepath;
};

export
const wspath = () => {
    return (window as any).CONNECTION_CONFIG.wspath;
};
