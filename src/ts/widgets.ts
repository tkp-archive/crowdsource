import {Widget} from "@phosphor/widgets";

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
            "<p>Crowdsource is a streaming competition engine</p>";
        return node;
    }

   export function createRegisterNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<label>Register</label> \
            <input type=\"text\" placeholder=\"username\"></input>\
            <label>Email</label> \
            <input type=\"email\" placeholder=\"email\"></input>\
            <label>Password</label> \
            <input type=\"password\" placeholder=\"password\"></input>\
            <input type=\"submit\" value=\"Register\"></input>";
        return node;
    }

   export function createLoginNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<label>Login</label> \
            <input type=\"text\" placeholder=\"username\"></input>\
            <label>Password</label> \
            <input type=\"password\" placeholder=\"password\"></input>\
            <input type=\"submit\" value=\"Login\"></input>";
        return node;
    }

   export function createLogoutNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<input type=\"submit\" value=\"Logout\"></input>";
        return node;
    }

}