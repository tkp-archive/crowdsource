/******************************************************************************
 *
 * Copyright (c) 2018, the Perspective Authors.
 *
 * This file is part of the Perspective library, distributed under the terms of
 * the Apache License 2.0.  The full license can be found in the LICENSE file.
 *
 */

import perspective from "@finos/perspective";
import {PerspectiveWorkspace, PerspectiveWidget} from "@finos/perspective-phosphor";
import {Widget} from "@phosphor/widgets";

import "@finos/perspective-viewer-hypergrid";
import "@finos/perspective-viewer-d3fc";

export
async function main() {
    const websocket = (perspective as any).websocket((window as any).CONNECTION_CONFIG.wspath + 'api/wscompetition');
    const table = websocket.open_table('data_source_one');

    const workspace = new PerspectiveWorkspace();
    const widget1 = new PerspectiveWidget("One");

    workspace.addViewer(widget1, {});
    // workspace.addViewer(widget2, {mode: "split-bottom", ref: widget1});
    Widget.attach(workspace, document.body);

    widget1.load(table);

    window.onresize = () => {
        workspace.update();
    };

    (window as any).workspace = workspace;
}
