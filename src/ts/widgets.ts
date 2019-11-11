import {Widget} from "@phosphor/widgets";
import {IRequestResult, request} from "requests-helper";
import {APIKEYS, LOGIN, LOGOUT, REGISTER} from "./define";
import {basepath} from "./utils";
// tslint:disable max-classes-per-file no-namespace no-empty object-literal-sort-keys no-console

export
class BaseWidget extends Widget {
    constructor(options: {node: HTMLDivElement}) {
        super(options);
    }

    protected getInput(): HTMLInputElement {
        return this.node.querySelector("input[type=submit]") as HTMLInputElement;
    }

    protected getForm(): HTMLFormElement {
        return this.node.querySelector("form") as HTMLFormElement;
    }
}

export
class AboutWidget extends BaseWidget {
    constructor() {
        super({node: Private.createAboutNode()});
        this.addClass("about");
        this.title.label = "About";
    }
}

export
class RegisterWidget extends BaseWidget {
    constructor() {
        super({node: Private.createRegisterNode()});
        this.getForm().onsubmit = (e) => this.register(e);
        this.addClass("register");
        this.title.label = "Register";
    }

    private getFormData(): {[key: string]: string} {
        return {username: (this.node.querySelector("input[type=text]") as HTMLInputElement).value,
                email: (this.node.querySelector("input[type=email]") as HTMLInputElement).value,
                password: (this.node.querySelector("input[type=password]") as HTMLInputElement).value};
    }

    private register(e: Event): void {
        e.preventDefault();
        request("post", basepath() + REGISTER, {}, this.getFormData()).then((res: IRequestResult) => {
            if (res.ok) {
                this.close();
            } else {
                console.error("register failed");
            }
        });
    }
}

export
class LoginWidget extends BaseWidget {
    constructor() {
        super({node: Private.createLoginNode()});
        this.getForm().onsubmit = (e) => this.login(e);
        this.addClass("login");
        this.title.label = "Login";
    }

    private getFormData(): {[key: string]: string} {
        return {username: (this.node.querySelector("input[type=text]") as HTMLInputElement).value,
                password: (this.node.querySelector("input[type=password]") as HTMLInputElement).value};
    }

    private login(e: Event): void {
        e.preventDefault();
        request("post", basepath() + LOGIN, {}, this.getFormData()).then((res: IRequestResult) => {
            if (res.ok) {
                const username = (res.json() as {[key: string]: string}).username;
                (window as any).user = username;
                this.close();
            } else {
                console.error("login failed");
            }
        });
    }
}

export
class LogoutWidget extends BaseWidget {
    constructor() {
        super({node: Private.createLogoutNode()});
        this.getForm().onsubmit = (e) => this.logout(e);
        this.addClass("logout");
        this.title.label = "Logout";
    }

    private logout(e: Event): void {
        e.preventDefault();
        request("post", basepath() + LOGOUT).then((res: IRequestResult) => {
            if (res.ok) {
                (window as any).user = undefined;
                this.close();
            } else {
                console.error("logout failed");
            }
        });
    }
}

export
class APIKeysWidget extends BaseWidget {
    constructor() {
        super({node: Private.createAPIKeysNode()});
        this.getForm().onsubmit = (e) => this.newKey(e);
        this.addClass("apikeys");
        this.title.label = "API Keys";
    }

    public onAfterAttach() {
        request("get", basepath() + APIKEYS).then((res: IRequestResult) => {
            if (res.ok) {
                const table = this.getTable();
                while (table.lastChild) {
                    table.removeChild(table.lastChild);
                }
                const data = res.json() as {[key: string]: {[key: string]: string}};
                let count = 0;
                for (const k of Object.keys(data)) {
                    const dat = data[k];
                    Private.addAPIKeyTableRow(table, dat.apikey_id, dat.key, dat.secret, (id: string) => {
                        request("post", basepath() + APIKEYS, {id}).then((res2: IRequestResult) => {
                            if (res2.ok) {
                                this.onAfterAttach();
                            } else {
                                console.error("apikey delete failed");
                            }
                        });
                    });
                    count++;
                }
                if (count === 0) {
                    Private.addAPIKeyTableRow(table, "-", "-", "-", (id: string) => {});
                }
            }
        });
    }

    private getTable(): HTMLDivElement {
        return this.node.querySelector("div.table") as HTMLDivElement;
    }

    private newKey(e: Event): void {
        e.preventDefault();
        request("post", basepath() + APIKEYS).then((res: IRequestResult) => {
            if (res.ok) {
                this.onAfterAttach();
            } else {
                console.error("apikeys failed");
            }
        });
    }
}

export
class SubmissionsWidget extends BaseWidget {
    constructor() {
        super({node: Private.createSubmissionsNode()});
        // this.getForm().onsubmit = (e) => this.logout(e);
        this.addClass("submissions");
        this.title.label = "Submissions";

    }
}

namespace Private {
    export function createAboutNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<div>\
            <p>Crowdsource is a streaming competition engine</p>\
            </div>";
        return node;
    }

    export function createRegisterNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<form name=\"register\" action=\"\">\
            <label>Register</label> \
            <input type=\"text\" placeholder=\"username\" autocomplete=\"username\" required></input>\
            <label>Email</label> \
            <input type=\"email\" placeholder=\"email\" required></input>\
            <label>Password</label> \
            <input type=\"password\" placeholder=\"password\" autocomplete=\"new-password\" required></input>\
            <input type=\"submit\" value=\"Register\"></input>\
            </form>";
        return node;
    }

    export function createLoginNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<form name=\"login\" action=\"\">\
            <label>Login</label> \
            <input type=\"text\" placeholder=\"username\" autocomplete=\"username\" required></input>\
            <label>Password</label> \
            <input type=\"password\" placeholder=\"password\" autocomplete=\"current-password\" required></input>\
            <input type=\"submit\" value=\"Login\"></input>\
            </form>";
        return node;
    }

    export function createLogoutNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<form name=\"logout\" action=\"\">\
            <input type=\"submit\" value=\"Logout\"></input>\
            </form>";
        return node;
    }

    export function createAPIKeysNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<h2>Active Keys</h2>\
            <div class=\"table\"></div> \
            <h2>Create New</h2>\
            <form name=\"apikey\" action=\"\">\
            <input type=\"submit\" value=\"Create\"></input>\
            </form>";
        return node;
    }

    export function createSubmissionsNode(): HTMLDivElement {
        const node = document.createElement("div");
        return node;
    }

    export function addAPIKeyTableRow(table: HTMLDivElement,
                                      id: string,
                                      key: string,
                                      secret: string,
                                      ondelete: (id: string) => void) {
        const row = document.createElement("div");
        row.innerHTML =
            "<div>\
            <label>Id:</label>\
            <label>" + id + "</label>\
            </div>\
            <div>\
            <label>Key:</label>\
            <input type=\"text\" value=\"" + key + "\"></input>\
            </div>\
            <div>\
            <label>Secret:</label>\
            <input type=\"text\" value=\"" + secret + "\"></input>\
            </div>\
            <div>\
            <label>Delete:</label>\
            <input type=\"submit\" value=\"Delete\"></input>\
            </div>";
        (row.querySelector("input[type=submit]") as HTMLInputElement).onclick = (e: Event) => ondelete(id);
        table.appendChild(row);
    }

}
