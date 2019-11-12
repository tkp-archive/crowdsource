import {IRequestResult, request} from "requests-helper";
import {LOGIN} from "./define";

export
const loggedIn = () => {
    return (window as any).user;
};

export
const checkLoggedIn = async () => {
    request("post", basepath() + LOGIN, {}, {}).then((res: IRequestResult) => {
        if (res.ok) {
            const username = (res.json() as {[key: string]: string}).username;
            (window as any).user = username;
            return username;
        } else {
            return undefined;
        }
    });
};

export
const basepath = () => {
    return (window as any).CONNECTION_CONFIG.basepath;
};

export
const wspath = () => {
    return (window as any).CONNECTION_CONFIG.wspath;
};
