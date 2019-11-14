import {BaseWidget} from "./base";

// tslint:disable no-namespace

export
class CompetitionsWidget extends BaseWidget {
    constructor() {
        super({node: Private.createCompetitionsNode()});
        // this.getForm().onsubmit = (e) => this.logout(e);
        this.addClass("competitions");
        this.title.label = "Competitions";

    }
}

namespace Private {
    export function createCompetitionsNode(): HTMLDivElement {
        const node = document.createElement("div");
        return node;
    }
}
