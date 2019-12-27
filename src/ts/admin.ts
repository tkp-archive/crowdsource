import {PerspectiveWidget} from "@finos/perspective-phosphor";
import {DockPanel, SplitPanel, Widget} from "@phosphor/widgets";
// import {request, IRequestResult} from "requests-helper";
// tslint:disable no-empty no-namespace max-classes-per-file

export class AdminWidget extends DockPanel {
    constructor() {
      super();
      this.addClass("admin");
      this.title.label = "Admin";
      this.title.closable = true;
      this.addWidget(new AdminControlsWidget("Clients"));
      this.addWidget(new AdminControlsWidget("Competitions"));
      this.addWidget(new AdminControlsWidget("Submissions"));
    }

}

export class AdminControlsWidget extends SplitPanel {
  constructor(title: string) {
    super({orientation: "vertical"});
    this.title.label = title;
    this.title.closable = false;

    this.addWidget(new ConstrolsWidget(title));
    this.addWidget(new PerspectiveWidget(title));
    this.setRelativeSizes([1, 3]);
  }
}

export class ConstrolsWidget extends Widget {
  constructor(title: string) {
    super({node: Private.createControlsNode(title)});
  }
}

namespace Private {
  export
  function createControlsNode(title: string): HTMLDivElement {
    const ret = document.createElement("div");
    ret.innerHTML =
      `<div>\
      <h2>${title}</h2>\
      </div>`;
    return ret;
  }
}
