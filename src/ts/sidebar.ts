import {each} from "@phosphor/algorithm";
import {DockPanel, Widget} from "@phosphor/widgets";


export class SidebarPanel extends DockPanel {
    private _closeCallback = (panel: SidebarPanel) => {};

    constructor(name: string, widget: Widget, closeCallback = (panel: SidebarPanel) => {}){
        super({mode: "single-document"});
        widget.title.closable = true;
        widget.title.label = name;
        this._closeCallback = closeCallback;
        this.addWidget(widget);
        each(this.tabBars(), (t) => {
            t.show();
        });
    }

  protected onChildRemoved(msg: Widget.ChildMessage): void {
      super.onChildRemoved(msg);
      if(this.isEmpty){
          this._closeCallback(this);
      }
  }

}