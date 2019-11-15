import {IRequestResult, request} from "requests-helper";
import {REGISTER} from "../define";
import {basepath} from "../utils";
import {BaseWidget} from "./base";
// tslint:disable no-namespace object-literal-sort-keys no-console

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

namespace Private {
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
}
