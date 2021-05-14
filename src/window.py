# window.py
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

from gi.repository import Adw, Gtk, Gio

from breathing.timer import Timer


@Gtk.Template(resource_path='/io/github/seadve/Breathing/ui/window.ui')
class BreathingWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BreathingWindow'

    main_button = Gtk.Template.Child()
    button_stack = Gtk.Template.Child()
    circle1 = Gtk.Template.Child()
    circle2 = Gtk.Template.Child()
    circle3 = Gtk.Template.Child()
    dark_mode_button = Gtk.Template.Child()
    time_label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = Timer(self.button_stack, self)
        self.settings = Gio.Settings("io.github.seadve.Breathing")
        self.settings.bind(
            "dark-mode", self.get_settings(),
            "gtk-application-prefer-dark-theme", Gio.SettingsBindFlags.DEFAULT
        )
        self.setup_darkmode()

    def enlarge_circles(self):
        self.circle1.get_style_context().add_class("enlarge1")
        self.circle2.get_style_context().add_class("enlarge2")
        self.circle3.get_style_context().add_class("enlarge3")

    def smallify_circles(self):
        self.circle1.get_style_context().add_class("smallify")
        self.circle2.get_style_context().add_class("smallify")
        self.circle3.get_style_context().add_class("smallify")

    def clean_circles(self):
        self.circle1.get_style_context().remove_class("smallify")
        self.circle2.get_style_context().remove_class("smallify")
        self.circle3.get_style_context().remove_class("smallify")
        self.circle1.get_style_context().remove_class("enlarge1")
        self.circle2.get_style_context().remove_class("enlarge2")
        self.circle3.get_style_context().remove_class("enlarge3")

    def set_button_play_mode(self, is_play):
        if is_play:
            self.main_button.get_style_context().remove_class("suggested-action")
            self.main_button.get_style_context().add_class("playing")
        else:
            self.main_button.get_style_context().add_class("suggested-action")
            self.main_button.get_style_context().remove_class("playing")

    def setup_darkmode(self):
        dark_mode = self.settings.get_boolean("dark-mode")
        if dark_mode:
            self.dark_mode_button.set_icon_name("dark-mode-symbolic")
        else:
            self.dark_mode_button.set_icon_name("light-mode-symbolic")

    def toggle_dark_mode(self):
        dark_theme = self.dark_mode_button.get_icon_name() == "light-mode-symbolic"
        if dark_theme:
            self.dark_mode_button.set_icon_name("dark-mode-symbolic")
        else:
            self.dark_mode_button.set_icon_name("light-mode-symbolic")
        self.settings.set_boolean("dark-mode", dark_theme)

    def toggle_breathing(self):
        if self.timer.time == 0:
            self.timer.start()
        else:
            self.timer.cancel()
