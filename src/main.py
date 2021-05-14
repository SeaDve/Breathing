# main.py
#
# Copyright 2021 SeaDve
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

        Gio.Settings.new('io.github.seadve.Breathing')
        self.setup_actions()

        Adw.init()

    def setup_actions(self):
        simple_actions = [
            ("toggle-dark-mode", self.window_toggle_dark_mode, ("<Ctrl>d",)),
            ("toggle-breathing", self.window_toggle_breathing, ("<Ctrl>s",)),
            ("show-shortcuts", self.show_shortcuts_window, ("<Ctrl>question",)),
            ("show-about", self.show_about_dialog, None),
            ("quit", lambda *_: self.quit(), ("<Ctrl>q",)),
        ]

        for action, callback, accel in simple_actions:
            simple_action = Gio.SimpleAction.new(action, None)
            simple_action.connect("activate", callback)
            self.add_action(simple_action)
            if accel:
                self.set_accels_for_action(f"app.{action}", accel)

    def window_toggle_dark_mode(self, action, param):
        self.get_active_window().toggle_dark_mode()

    def window_toggle_breathing(self, action, param):
        self.get_active_window().toggle_breathing()

    def show_shortcuts_window(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource('/io/github/seadve/Breathing/ui/shortcuts.ui')
        window = builder.get_object('shortcuts')
        window.set_transient_for(self.get_active_window())
        window.present()

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
        about.show()


def main(version):
    app = Application(version)
    return app.run(sys.argv)
