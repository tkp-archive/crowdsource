import {each} from "@phosphor/algorithm";
import {DockPanel, Widget} from "@phosphor/widgets";
// tslint:disable no-empty variable-name

export class SidebarPanel extends DockPanel {

    constructor(closeCallback = (panel: SidebarPanel) => {}) {
        super({mode: "single-document"});
        this._closeCallback = closeCallback;
        this.addClass("sidebar");
    }

  public addWidget(w: Widget) {
      w.title.closable = true;
      w.addClass("sidebar");
      super.addWidget(w);
      each(this.tabBars(), (t) => {
        t.show();
      });

  }

  protected onChildRemoved(msg: Widget.ChildMessage): void {
      super.onChildRemoved(msg);
      if (this.isEmpty) {
          this._closeCallback(this);
      }
  }

  private _closeCallback = (panel: SidebarPanel) => {};

}
