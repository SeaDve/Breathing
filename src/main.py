# SPDX-FileCopyrightText: Copyright 2021 SeaDve
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw

from breathing.window import BreathingWindow

APPLICATION_ID = "io.github.seadve.Breathing"

class Application(Adw.Application):
    def __init__(self, version):
        super().__init__(application_id=APPLICATION_ID,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.version = version
        self.settings = Gio.Settings.new(APPLICATION_ID)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = BreathingWindow(application=self)
        win.present()

    def do_startup(self):
        Adw.Application.do_startup(self)

        Gtk.Window.set_default_icon_name(APPLICATION_ID)

        self.setup_actions()

    def setup_actions(self):
        simple_action = Gio.SimpleAction.new("toggle-breathing", None)
        simple_action.connect("activate", self.window_toggle_breathing)
        self.add_action(simple_action)

        simple_action = Gio.SimpleAction.new("show-about", None)
        simple_action.connect("activate", self.show_about_dialog)
        self.add_action(simple_action)

        simple_action = Gio.SimpleAction.new("quit", None)
        simple_action.connect("activate", lambda *_: self.quit())
        self.add_action(simple_action)

        settings_action = self.settings.create_action('dark-mode')
        self.add_action(settings_action)

        self.set_accels_for_action("app.toggle-breathing", ("<Ctrl>s",))
        self.set_accels_for_action("app.dark-mode", ("<Ctrl>d",))
        self.set_accels_for_action("app.quit", ("<Ctrl>q",))

    def window_toggle_dark_mode(self, action, param):
        self.settings.set_boolean("dark-mode", False)

    def window_toggle_breathing(self, action, param):
        self.get_active_window().toggle_breathing()

    def show_about_dialog(self, action, param):
        about = Adw.AboutWindow()
        about.set_modal(True)
        about.set_transient_for(self.get_active_window())
        about.set_application_icon(APPLICATION_ID)
        about.set_application_name("Breathing")
        about.set_developer_name("Dave Patrick Caberto")
        about.set_version(self.version)
        about.set_copyright(_("© 2023 Dave Patrick Caberto"))
        about.set_license_type(Gtk.License.GPL_3_0)
        # Translators: Replace "translator-credits" with your names, one name per line
        about.set_translator_credits(_("translator-credits"))
        about.set_issue_url("https://github.com/SeaDve/Breathing/issues")
        about.set_support_url("https://github.com/SeaDve/Breathing/discussions")

        about.add_link(_("Donate (Buy Me a Coffee)"), "https://www.buymeacoffee.com/seadve")
        about.add_link(_("GitHub"), "https://github.com/SeaDve/Breathing")
        about.add_link(_("Translate"), "https://hosted.weblate.org/projects/kooha/breathing")

        about.present()


def main(version):
    app = Application(version)
    return app.run(sys.argv)
