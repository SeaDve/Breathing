# SPDX-FileCopyrightText: Copyright 2021 SeaDve
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Gdk, GLib, Adw

from breathing.window import BreathingWindow


class Application(Gtk.Application):
    def __init__(self, version):
        super().__init__(application_id='io.github.seadve.Breathing',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.version = version

        GLib.set_application_name("Breathing")
        GLib.set_prgname('io.github.seadve.Breathing')

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = BreathingWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/io/github/seadve/Breathing/ui/style.css')
        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.settings = Gio.Settings.new('io.github.seadve.Breathing')
        self.setup_actions()

        Adw.init()

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
        about = Gtk.AboutDialog()
        about.set_transient_for(self.get_active_window())
        about.set_modal(True)
        about.set_version(self.version)
        about.set_program_name("Breathing")
        about.set_logo_icon_name("io.github.seadve.Breathing")
        about.set_authors(["Dave Patrick"])
        about.set_comments(_("Exercise your breathing"))
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_copyright(_("Copyright 2021 Dave Patrick"))
        # Translators: Replace "translator-credits" with your names, one name per line
        about.set_translator_credits(_("translator-credits"))
        about.set_website_label(_("GitHub"))
        about.set_website("https://github.com/SeaDve/Breathing")
        about.present()


def main(version):
    app = Application(version)
    return app.run(sys.argv)
