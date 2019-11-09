import {Widget} from "@phosphor/widgets";

export
class AboutWidget extends Widget {
    constructor() {
        super({node: Private.createAboutNode()});
        this.addClass("about");
    }
}

namespace Private {
    export function createAboutNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<div><p>Crowdsource is a streaming competition engine</p></div>";
        return node;
    }
}