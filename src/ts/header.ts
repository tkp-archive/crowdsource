import {Widget} from "@phosphor/widgets";
import {basepath} from "./utils";

export
class Header extends Widget {
    public static createNode(): HTMLElement {
        const node = document.createElement("div");
        node.classList.add("header");
        const a = document.createElement("a");
        a.href = basepath();

        const img = document.createElement("img");
        img.src = a.href + "static/img/cs_cyan.png";
        a.appendChild(img);
        node.appendChild(a);

        const username = document.createElement("span");
        username.textContent = (document as any).user;
        username.classList.add("username");

        node.appendChild(username);
        return node;
    }

    constructor() {
        super({ node: Header.createNode() });
        this.setFlag(Widget.Flag.DisallowLayout);
        this.title.closable = false;
    }
}
