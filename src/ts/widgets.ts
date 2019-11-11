import {Widget} from "@phosphor/widgets";
import {IRequestResult, request} from "requests-helper";
import {LOGIN, LOGOUT, REGISTER} from "./define";
import {basepath} from "./utils";
// tslint:disable max-classes-per-file no-namespace no-empty object-literal-sort-keys

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

    private register(e: Event): boolean {
        e.preventDefault();
        request("post", basepath() + REGISTER, {}, this.getFormData()).then((res: IRequestResult) => {
            if (res.ok) {
                this.close();
            } else {
                console.error("register failed");
            }
        });
        return false;
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

    private login(e: Event): boolean {
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
        return false;
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

    private logout(e: Event): boolean {
        e.preventDefault();
        request("post", basepath() + LOGOUT).then((res: IRequestResult) => {
            if (res.ok) {
                (window as any).user = undefined;
                this.close();
            } else {
                console.error("logout failed");
            }
        });
        return true;
    }
}

export
class APIKeysWidget extends BaseWidget {
    constructor() {
        super({node: Private.createAPIKeysNode()});
        // this.getForm().onsubmit = (e) => this.logout(e);
        this.addClass("apikeys");
        this.title.label = "API Keys";
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
        return node;
    }

    export function createSubmissionsNode(): HTMLDivElement {
        const node = document.createElement("div");
        return node;
    }

}
