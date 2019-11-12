import {BaseWidget} from "./base";

// tslint:disable no-namespace

export
class AboutWidget extends BaseWidget {
    constructor() {
        super({node: Private.createAboutNode()});
        this.addClass("about");
        this.title.label = "About";
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
}
