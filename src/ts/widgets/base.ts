import {Widget} from "@phosphor/widgets";

export
class BaseWidget extends Widget {
    constructor(options: {node: HTMLDivElement}) {
        super(options);
    }

    protected getInput(): HTMLInputElement {
        return this.node.querySelector("input[type=submit]") as HTMLInputElement;
    }

    protected getForm(): HTMLFormElement {
        return this.node.querySelector("form") as HTMLFormElement;
    }
}
