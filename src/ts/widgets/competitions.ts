import {PerspectiveWidget} from "@finos/perspective-phosphor";
import {SplitPanel} from "@phosphor/widgets";
import {IRequestResult, request} from "requests-helper";
import {COMPETITIONS} from "../define";
import {basepath, loggedIn} from "../utils";
// tslint:disable no-namespace no-console

export
class CompetitionsWidget extends SplitPanel {
    constructor() {
        super();
        this.addClass("competitions");
        this.title.label = "My Competitions";
        this.title.closable = true;
    }

    public onAfterAttach() {
        request("get", basepath() + COMPETITIONS, {client_username: loggedIn()}).then((res: IRequestResult) => {
            if (res.ok) {
                const data = res.json() as any;
                const widget = new PerspectiveWidget("Competitions");
                this.addWidget(widget);
                widget.load(data);
            } else {
                console.error("competitions get failed");
            }
        });
    }
}
