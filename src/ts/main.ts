/******************************************************************************
 *
 * Copyright (c) 2018, the Perspective Authors.
 *
 * This file is part of the Perspective library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */

import perspective from "@finos/perspective";
import {PerspectiveWidget, PerspectiveWorkspace} from "@finos/perspective-phosphor";
import {MenuBar, Widget} from "@phosphor/widgets";
import {Header} from "./header";
import {buildMenubar} from "./menu";

import "@finos/perspective-viewer-d3fc";
import "@finos/perspective-viewer-hypergrid";

export
async function main() {
    const websocket = (perspective as any).websocket((window as any).CONNECTION_CONFIG.wspath + "api/v1/wscompetition");
    const table1 = websocket.open_table("competitions");
    const table2 = websocket.open_table("submissions");

    const workspace = new PerspectiveWorkspace();
    const widget1 = new PerspectiveWidget("Competitions");
    const widget2 = new PerspectiveWidget("Leaderboards");
    const header = new Header();
    const menubar = new MenuBar();

    menubar.addClass("topmenu");
    buildMenubar(menubar);

    workspace.addViewer(widget1, {});
    workspace.addViewer(widget2, {mode: "split-bottom", ref: widget1});

    Widget.attach(header, document.body);
    Widget.attach(menubar, document.body);
    Widget.attach(workspace, document.body);

    widget1.load(table1);
    widget2.load(table2);

    window.onresize = () => {
        workspace.update();
    };

    (window as any).workspace = workspace;
}
