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

    private login(e: Event): boolean {
        request("post", basepath() + LOGIN, {}, this.getFormData()).then((res: IRequestResult) => {
            if (res.ok) {
                this.close();
            } else {
                console.error("login failed");
            }
        });
        return true;
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
        request("post", basepath() + LOGOUT).then((res: IRequestResult) => {
            if (res.ok) {
                this.close();
            } else {
                console.error("logout failed");
            }
        });
        return true;
    }
}

namespace Private {
    export function createLoginNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<form name=\"login\" action=\"" + basepath() + LOGIN + "\">\
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
            "<form name=\"logout\" action=\"" + basepath() + LOGOUT + "\">\
            <input type=\"submit\" value=\"Logout\"></input>\
            </form>";
        return node;
    }
}
