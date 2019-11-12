import {BaseWidget} from "./base";

// tslint:disable max-classes-per-file no-namespace no-empty

export
class NewCompetitionWidget extends BaseWidget {
    constructor() {
        super({node: Private.createNewCompetitionNode()});
        // this.getForm().onsubmit = (e) => this.logout(e);
        this.addClass("newcompetition");
        this.title.label = "New Competition";

    }
}

export
class NewSubmissionWidget extends BaseWidget {
    constructor() {
        super({node: Private.createNewSubmissionNode()});
        // this.getForm().onsubmit = (e) => this.logout(e);
        this.addClass("newsubmission");
        this.title.label = "New Submission";

    }
}

namespace Private {
    export function createNewCompetitionNode(): HTMLDivElement {
        const node = document.createElement("div");
        return node;
    }

    export function createNewSubmissionNode(): HTMLDivElement {
        const node = document.createElement("div");
        return node;
    }
}
