// tslint:disable: no-empty
import perspective from "@finos/perspective";
import {PerspectiveWidget, PerspectiveWorkspace} from "@finos/perspective-phosphor";
import {CommandRegistry} from "@phosphor/commands";
import {BoxPanel, Menu, MenuBar, SplitPanel, Widget} from "@phosphor/widgets";
import {AboutWidget} from "./widgets";
import {Header} from "./header";
import {SidebarPanel} from "./sidebar";

import "@finos/perspective-viewer-d3fc";
import "@finos/perspective-viewer-hypergrid";

export const commands = new CommandRegistry();

export
async function main() {
    // connect to perspective
    const websocket = (perspective as any).websocket((window as any).CONNECTION_CONFIG.wspath + "api/v1/wscompetition");
    const table1 = websocket.open_table("competitions");
    const table2 = websocket.open_table("submissions");

    // perspective workspace
    const workspace = new PerspectiveWorkspace();
    const widget1 = new PerspectiveWidget("Competitions");
    const widget2 = new PerspectiveWidget("Leaderboards");

    // top bar
    const header = new Header();
    // top right menu
    const menubar = new MenuBar();

    // configuration pages
    const login = new BoxPanel();
    const logout = new BoxPanel();
    const register = new BoxPanel();
    const apikeys = new BoxPanel();
    const submissions = new PerspectiveWidget("Submissions");
    const about = new AboutWidget();

    // main container
    const main = new SplitPanel({orientation: "horizontal"});
    main.addWidget(workspace);

    // to track whats in side bar
    let side_panel: Widget = null;

    // helper to clear sidebar
    const setSidePanel = (name: string, w: Widget) => {
        if (side_panel){
            side_panel.close();
        }
        const sidebar = new SidebarPanel(name, w, (s: SidebarPanel) => {
            s.close();
            main.setRelativeSizes([1]);
        });
        sidebar.addClass("sidebar");
        main.addWidget(sidebar);
        main.setRelativeSizes([3, 1]);
        side_panel = sidebar;
    };


    /* 
     *  Commands
     */
    commands.addCommand("about", {
        execute: () => {setSidePanel("About", about)},
        iconClass: "fa fa-question",
        isEnabled: () => true,
        label: "About",
    });

    commands.addCommand("register", {
        execute: () => {setSidePanel("Register", register)},
        iconClass: "fa fa-plus",
        isEnabled: () => true,
        label: "Register",
    });

    commands.addCommand("login", {
        execute: () => {setSidePanel("Login", login)},
        iconClass: "fa fa-sign-in",
        isEnabled: () => true,
        label: "Login",
    });

    commands.addCommand("logout", {
        execute: () => {setSidePanel("Logout", logout)},
        iconClass: "fa fa-sign-out",
        isEnabled: () => false,
        label: "Logout",
    });

    commands.addCommand("apikeys", {
        execute: () => {setSidePanel("API Keys", apikeys)},
        iconClass: "fa fa-cog",
        isEnabled: () => false,
        label: "API Keys",
    });

    commands.addCommand("submissions", {
        execute: () => {setSidePanel("Submissions", submissions)},
        iconClass: "fa fa-paper-plane",
        isEnabled: () => false,
        label: "Submissions",
    });

    // Construct top menu
    menubar.addClass("topmenu");
    const menu = new Menu({commands});
    menu.addClass("settings");
    menu.title.label = "Settings";
    menu.title.mnemonic = 0;
    menu.addItem({ command: "about"});
    menu.addItem({ command: "register"});
    menu.addItem({ command: "login"});
    menu.addItem({ command: "logout"});
    menu.addItem({ command: "apikeys"});
    menu.addItem({ command: "submissions"});
    menubar.addMenu(menu);

    // Add tables to workspace
    workspace.addViewer(widget1, {});
    workspace.addViewer(widget2, {mode: "split-bottom", ref: widget1});

    // Attach parts to dom
    Widget.attach(header, document.body);
    Widget.attach(menubar, document.body);
    Widget.attach(main, document.body);

    // Load perspective tables
    widget1.load(table1);
    widget2.load(table2);

    window.onresize = () => {
        workspace.update();
    };

    (window as any).workspace = workspace;
}
