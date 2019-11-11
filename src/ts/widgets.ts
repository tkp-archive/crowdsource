import {Widget} from "@phosphor/widgets";

// tslint:disable max-classes-per-file no-namespace

export
class AboutWidget extends Widget {
    constructor() {
        super({node: Private.createAboutNode()});
        this.addClass("about");
    }
}

export
class RegisterWidget extends Widget {
    constructor() {
        super({node: Private.createRegisterNode()});
        this.addClass("register");
    }
}

export
class LoginWidget extends Widget {
    constructor() {
        super({node: Private.createLoginNode()});
        this.addClass("login");
    }
}

export
class LogoutWidget extends Widget {
    constructor() {
        super({node: Private.createLogoutNode()});
        this.addClass("logout");
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
            "<div>\
            <label>Register</label> \
            <input type=\"text\" placeholder=\"username\"></input>\
            <label>Email</label> \
            <input type=\"email\" placeholder=\"email\"></input>\
            <label>Password</label> \
            <input type=\"password\" placeholder=\"password\"></input>\
            <input type=\"submit\" value=\"Register\"></input>\
            </div>";
        return node;
    }

    export function createLoginNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<div>\
            <label>Login</label> \
            <input type=\"text\" placeholder=\"username\"></input>\
            <label>Password</label> \
            <input type=\"password\" placeholder=\"password\"></input>\
            <input type=\"submit\" value=\"Login\"></input>\
            </div>";
        return node;
    }

    export function createLogoutNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<div>\
            <input type=\"submit\" value=\"Logout\"></input>\
            </div>";
        return node;
    }

}
