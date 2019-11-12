import {IRequestResult, request} from "requests-helper";
import {APIKEYS} from "../define";
import {basepath} from "../utils";
import {BaseWidget} from "./base";

// tslint:disable no-namespace no-empty no-console

export
class APIKeysWidget extends BaseWidget {
    constructor() {
        super({node: Private.createAPIKeysNode()});
        this.getForm().onsubmit = (e) => this.newKey(e);
        this.addClass("apikeys");
        this.title.label = "API Keys";
    }

    public onAfterAttach() {
        request("get", basepath() + APIKEYS).then((res: IRequestResult) => {
            if (res.ok) {
                const table = this.getTable();
                while (table.lastChild) {
                    table.removeChild(table.lastChild);
                }
                const data = res.json() as {[key: string]: {[key: string]: string}};
                let count = 0;
                for (const k of Object.keys(data)) {
                    const dat = data[k];
                    Private.addAPIKeyTableRow(table, dat.apikey_id, dat.key, dat.secret, (id: string) => {
                        request("post", basepath() + APIKEYS, {id}).then((res2: IRequestResult) => {
                            if (res2.ok) {
                                this.onAfterAttach();
                            } else {
                                console.error("apikey delete failed");
                            }
                        });
                    });
                    count++;
                }
                if (count === 0) {
                    Private.addAPIKeyTableRow(table, "-", "-", "-", (id: string) => {});
                }
            }
        });
    }

    private getTable(): HTMLDivElement {
        return this.node.querySelector("div.table") as HTMLDivElement;
    }

    private newKey(e: Event): void {
        e.preventDefault();
        request("post", basepath() + APIKEYS).then((res: IRequestResult) => {
            if (res.ok) {
                this.onAfterAttach();
            } else {
                console.error("apikeys failed");
            }
        });
    }
}

namespace Private {
    export function createAPIKeysNode(): HTMLDivElement {
        const node = document.createElement("div");
        node.innerHTML =
            "<h2>Active Keys</h2>\
            <div class=\"table\"></div> \
            <h2>Create New</h2>\
            <form name=\"apikey\" action=\"\">\
            <input type=\"submit\" value=\"Create\"></input>\
            </form>";
        return node;
    }

    export function addAPIKeyTableRow(table: HTMLDivElement,
                                      id: string,
                                      key: string,
                                      secret: string,
                                      ondelete: (id: string) => void) {
        const row = document.createElement("div");
        row.innerHTML =
            "<div>\
            <label>Id:</label>\
            <label>" + id + "</label>\
            </div>\
            <div>\
            <label>Key:</label>\
            <input type=\"text\" value=\"" + key + "\"></input>\
            </div>\
            <div>\
            <label>Secret:</label>\
            <input type=\"text\" value=\"" + secret + "\"></input>\
            </div>\
            <div>\
            <label>Delete:</label>\
            <input type=\"submit\" value=\"Delete\"></input>\
            </div>";
        (row.querySelector("input[type=submit]") as HTMLInputElement).onclick = (e: Event) => ondelete(id);
        table.appendChild(row);
    }

}
