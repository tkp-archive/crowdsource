import {IRequestResult, request} from "requests-helper";
import {LOGIN, LOGOUT} from "../define";
import {basepath} from "../utils";
import {BaseWidget} from "./base";

// tslint:disable max-classes-per-file no-namespace object-literal-sort-keys no-console

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

namespace Private {
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
}
