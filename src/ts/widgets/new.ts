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
        node.innerHTML =
        "<form name=\"newcompetition\" action=\"\">\
        <h2>New Competition</h2> \
        <label>Title</label> \
        <input type=\"text\" placeholder=\"title\" required></input>\
        \
        <label>Subtitle</label> \
        <input type=\"text\" placeholder=\"subtitle\"></input>\
        \
        <label>Type</label> \
        <select name=\"type\">\
            <option value=\"classify\" selected>Classify</option>\
            <option value=\"predict\">Predict</option>\
            <option value=\"cluster\">Cluster</option>\
        </select>\
        \
        <label>Expiration</label> \
        <input type=\"datetime-local\" required></input>\
        \
        <label>Prize</label> \
        <input type=\"number\" step=\".1\" min=\"0\" placeholder=\"prize\"></input>\
        \
        <label>Metric</label> \
        <select name=\"metric\">\
            <option value=\"logloss\" selected>Log Loss</option>\
            <option value=\"absdiff\">Absolute Diff</option>\
        </select>\
        \
        <label>Targets</label> \
        \
        <label>Dataset</label> \
        \
        <label>Dataset Type</label> \
        <select name=\"dataset_type\">\
            <option value=\"json\" selected>JSON</option>\
            <option value=\"csv\">CSV</option>\
        </select>\
        \
        <label>Dataset Kwargs</label> \
        \
        <label>Dataset Key</label> \
        \
        <label>Num Classes</label> \
        <input type=\"number\" step=\"1\" min=\"2\" placeholder=\"number of classes\"></input>\
        \
        <label>When</label> \
        <input type=\"datetime-local\" required></input>\
        \
        <label>Answer</label> \
        \
        <label>Answer Type</label> \
        <select name=\"answer_type\">\
            <option value=\"json\" selected>JSON</option>\
            <option value=\"csv\">CSV</option>\
        </select>\
        \
        <label>Answer Delay</label> \
        \
        <input type=\"submit\" value=\"Create\"></input>\
        </form>";
        return node;
    }

    export function createNewSubmissionNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
        "<form name=\"newsubmission\" action=\"\">\
        <h2>New Submission</h2> \
        <label>Competition ID</label> \
        <input type=\"number\" step=\"1\" min=\"2\" placeholder=\"competition id\"></input>\
        \
        <label>Answer</label> \
        \
        <label>Answer Type</label> \
        <select name=\"answer_type\">\
            <option value=\"json\" selected>JSON</option>\
            <option value=\"csv\">CSV</option>\
        </select>\
        \
        <input type=\"submit\" value=\"Submit\"></input>\
        </form>";
        return node;
    }
}
