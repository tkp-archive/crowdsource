import {BaseWidget} from "./base";

// tslint:disable no-namespace

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
    export function createSubmissionsNode(): HTMLDivElement {
        const node = document.createElement("div");
        return node;
    }
}
