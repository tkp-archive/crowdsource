import {PerspectiveWidget} from "@finos/perspective-phosphor";
import {SplitPanel} from "@phosphor/widgets";
import {IRequestResult, request} from "requests-helper";
import {SUBMISSIONS} from "../define";
import {basepath, loggedIn} from "../utils";
// tslint:disable no-namespace no-console

export
class SubmissionsWidget extends SplitPanel {
    constructor() {
        super();
        this.addClass("submissions");
        this.title.label = "My Submissions";
        this.title.closable = true;
    }

    public onAfterAttach() {
        request("get", basepath() + SUBMISSIONS, {client_username: loggedIn()}).then((res: IRequestResult) => {
            if (res.ok) {
                const data = res.json() as any;
                const widget = new PerspectiveWidget("Submissions");
                this.addWidget(widget);
                widget.load(data);
            } else {
                console.error("submissions get failed");
            }
        });
    }
}
