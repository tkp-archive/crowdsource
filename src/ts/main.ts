// tslint:disable: no-empty
// tslint:disable: max-line-length
import perspective from "@finos/perspective";
import {PerspectiveWidget, PerspectiveWorkspace} from "@finos/perspective-phosphor";
import {CommandRegistry} from "@phosphor/commands";
import {DockPanel, SplitPanel, Widget} from "@phosphor/widgets";
import {IRequestResult, request} from "requests-helper";
import {APIKeysWidget, basepath, buildMenubar, checkLoggedIn, constructCommands, Header, loggedIn, LoginWidget, LogoutWidget, RegisterWidget, setupSidepanel, wspath} from "tkp_utils";

import {AdminWidget} from "./admin";
import {ADMIN, APIKEYS, LOGIN, LOGOUT, REGISTER, WSCOMPETITIONS} from "./define";
import {AboutWidget, CompetitionsWidget, NewCompetitionWidget, NewSubmissionWidget, PaymentsWidget, SubmissionsWidget} from "./widgets";

import "@finos/perspective-viewer-d3fc";
import "@finos/perspective-viewer-hypergrid";

export const commands = new CommandRegistry();

export
async function main() {
    // see if logged in
    await checkLoggedIn(LOGIN);

    // connect to perspective
    const websocket = perspective.websocket(wspath() + WSCOMPETITIONS);

    const competitionsTable = websocket.open_table("competitions");
    const leaderboardsTable = websocket.open_table("leaderboards");

    // perspective workspace
    const workspace = new PerspectiveWorkspace();
    workspace.addClass("workspace");
    workspace.title.label = "Workspace";

    const competitionsWidget = new PerspectiveWidget("Active Competitions");
    const leaderboardsWidget = new PerspectiveWidget("Leaderboards");

    // top bar
    const header = new Header("static/img/cs_cyan.png");

    // configuration pages
    const about = new AboutWidget();
    const login = new LoginWidget(LOGIN);
    const logout = new LogoutWidget(LOGOUT);
    const register = new RegisterWidget(REGISTER);

    const apikeys = new APIKeysWidget(APIKEYS);
    const myCompetitions = new CompetitionsWidget();
    const mySubmissions = new SubmissionsWidget();
    const payments = new PaymentsWidget();

    const newcompetition = new NewCompetitionWidget();
    const newsubmission = new NewSubmissionWidget();

    // setup admin page
    const admin = new AdminWidget();

    // main container
    const mainPage = new SplitPanel({orientation: "horizontal"});
    const centerPage = new DockPanel();
    mainPage.addWidget(centerPage);
    centerPage.addWidget(workspace);

    // helper to clear sidebar
    const setSidePanel = setupSidepanel(mainPage);

    // setup commands
    constructCommands(commands, [
        {
            execute: () => { setSidePanel(about); },
            iconClass: "fa fa-question",
            isEnabled: () => true,
            label: "About",
            name: "about",
        },
        {
            execute: () => { setSidePanel(register); },
            iconClass: "fa fa-pencil-square-o",
            isEnabled: () => !loggedIn(),
            label: "Register",
            name: "register",
        },
        {
            execute: () => { setSidePanel(login); },
            iconClass: "fa fa-sign-in",
            isEnabled: () => !loggedIn(),
            label: "Login",
            name: "login",
        },
        {
            execute: () => { setSidePanel(logout); },
            iconClass: "fa fa-sign-out",
            isEnabled: loggedIn,
            label: "Logout",
            name: "logout",
        },
        {
            execute: () => { setSidePanel(apikeys); },
            iconClass: "fa fa-key",
            isEnabled: loggedIn,
            label: "API Keys",
            name: "my:apikeys",
        },
        {
            execute: () => {
                centerPage.addWidget(myCompetitions);
                centerPage.selectWidget(myCompetitions);
            },
            iconClass: "fa fa-hourglass-start",
            isEnabled: loggedIn,
            label: "My Competitions",
            name: "my:competitions",
        },
        {
            execute: () => {
                centerPage.addWidget(mySubmissions);
                centerPage.selectWidget(mySubmissions);
            },
            iconClass: "fa fa-paper-plane",
            isEnabled: loggedIn,
            label: "My Submissions",
            name: "my:submissions",
        },
        {
            execute: () => {setSidePanel(payments); },
            iconClass: "fa fa-credit-card",
            isEnabled: loggedIn,
            label: "Wallet",
            name: "my:payments",
        },
        {
            execute: () => {setSidePanel(newcompetition); },
            iconClass: "fa fa-plus",
            isEnabled: () => loggedIn(),
            label: "New Competition",
            name: "new:competition",
        },
        {
            execute: () => {setSidePanel(newsubmission); },
            iconClass: "fa fa-plus",
            isEnabled: () => loggedIn(),
            label: "New Submission",
            name: "new:submission",
            },
        {
            execute: () => {
                centerPage.addWidget(admin);
                centerPage.selectWidget(admin);
            },
            iconClass: "fa fa-cog",
            isEnabled: () => loggedIn(),
            label: "Admin",
            name: "admin",
        },
    ]);

    // Construct top menu
    const menubar = buildMenubar(commands, "Settings", "settings", [
      {
            class: "settings",
            commands: ["about"],
      },
      {
            class: "settings",
            commands: ["register", "login", "logout"],
            name: "Login/Register",
      },
      {
            class: "settings",
            commands: ["new:competition", "new:submission"],
            name: "New",
      },
      {
            class: "settings",
            commands: ["my:apikeys", "my:competitions", "my:submissions", "my:payments"],
            name: "Profile",
      },

    ]);
    menubar.addClass("topmenu");

    // get admin page
    request("get", basepath() + ADMIN).then((res: IRequestResult) => {
        if (res.ok && res.status === 200) {
            menubar.menus[0].addItem({ command: "admin"});
        }
    });

    // Add tables to workspace
    workspace.addViewer(competitionsWidget, {});
    workspace.addViewer(leaderboardsWidget, {mode: "split-bottom", ref: competitionsWidget});

    // Attach parts to dom
    Widget.attach(header, document.body);
    Widget.attach(menubar, document.body);
    Widget.attach(mainPage, document.body);

    // Load perspective tables
    competitionsWidget.load(competitionsTable);
    leaderboardsWidget.load(leaderboardsTable);

    window.onresize = () => {
        mainPage.update();
    };
    (window as any).workspace = workspace;
}
