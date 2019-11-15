import {BaseWidget} from "./base";

// tslint:disable no-namespace

export
class PaymentsWidget extends BaseWidget {
    constructor() {
        super({node: Private.createPaymentsNode()});
        // this.getForm().onsubmit = (e) => this.logout(e);
        this.addClass("payments");
        this.title.label = "payments";

    }
}

namespace Private {
    export function createPaymentsNode(): HTMLDivElement {
        const node = document.createElement("div");
        return node;
    }
}
