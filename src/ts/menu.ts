import {CommandRegistry} from "@phosphor/commands";
import {Menu, MenuBar} from "@phosphor/widgets";

export const commands = new CommandRegistry();


export
function buildMenubar(bar: MenuBar) {
    const menu = new Menu({commands});
    menu.addClass("settings");
    menu.title.label = "Settings";
    menu.title.mnemonic = 0;

    commands.addCommand("register", {
        execute: () => {},
        iconClass: "fa fa-plus",
        isEnabled: () => {return false;},
        label: "Register",
        mnemonic: 2,
    });

    commands.addCommand("login", {
        execute: () => {},
        iconClass: "fa fa-sign-in",
        isEnabled: () => {return false;},
        label: "Login",
        mnemonic: 2,
    });

    commands.addCommand("logout", {
        execute: () => {},
        iconClass: "fa fa-sign-out",
        isEnabled: () => {return false;},
        label: "Logout",
        mnemonic: 2,
    });

    commands.addCommand("apikeys", {
        execute: () => {},
        iconClass: "fa fa-cog",
        isEnabled: () => {return true;},
        label: "API Keys",
        mnemonic: 2,
    });

    commands.addCommand("submissions", {
        execute: () => {},
        iconClass: "fa fa-paper-plane",
        isEnabled: () => {return true;},
        label: "Submissions",
        mnemonic: 2,
    });
 
    menu.addItem({ command: "apikeys"});
    menu.addItem({ command: "submissions"});
    menu.addItem({ command: "register"});
    menu.addItem({ command: "login"});
    menu.addItem({ command: "logout"});

    bar.addMenu(menu);
}