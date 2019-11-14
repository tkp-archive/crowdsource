import {Widget} from "@phosphor/widgets";
// tslint:disable no-empty no-namespace

export class AdminWidget extends Widget {

    constructor() {
      super({node: Private.createNode()});
      this.addClass("admin");
      this.title.label = "Admin";
      this.title.closable = true;
    }

}

namespace Private {
  export
  function createNode(): HTMLDivElement {
    const ret = document.createElement("div");
    ret.innerHTML =
      "<div>\
      <h2>Clients</h2>\
      </div>\
      <div>\
      <h2>Competitions</h2>\
      </div>\
      <div>\
      <h2>Submissions</h2>\
      </div>\
      <div>\
      <h2>Leaderboards</h2>\
      </div>\
      ";
    return ret;
  }
}
