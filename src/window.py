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

from gi.repository import Adw, Gtk, Gio, GObject

from breathing.timer import Timer


@Gtk.Template(resource_path='/io/github/seadve/Breathing/ui/window.ui')
class BreathingWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BreathingWindow'

    main_button = Gtk.Template.Child()
    button_stack = Gtk.Template.Child()
    circle1 = Gtk.Template.Child()
    circle2 = Gtk.Template.Child()
    circle3 = Gtk.Template.Child()
    time_label = Gtk.Template.Child()

    dark_mode = GObject.Property(type=bool, default=False, flags=GObject.ParamFlags.READWRITE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = Timer()
        self.settings = Gio.Settings("io.github.seadve.Breathing")
        self.get_settings().bind_property("gtk-application-prefer-dark-theme", self, "dark-mode")
        self.settings.bind(
            "dark-mode", self.get_settings(),
            "gtk-application-prefer-dark-theme", Gio.SettingsBindFlags.DEFAULT
        )
        self.connect_signals()

    @Gtk.Template.Callback()
    def get_dark_mode_icon(self, window, dark_mode):
        return "dark-mode-symbolic" if dark_mode else "light-mode-symbolic"

    def connect_signals(self):
        self.timer.connect('inhale', self.on_inhale)
        self.timer.connect('exhale', self.on_exhale)
        self.timer.connect('next-iter', self.on_next_iter)
        self.timer.connect('stopped', self.on_stopped)
        self.timer.connect('notify::time-remaining', self.on_time_changed)

    def on_inhale(self, timer):
        self._enlarge_circles()
        self.button_stack.set_visible_child_name('inhale')

    def on_exhale(self, timer):
        self._smallify_circles()
        self.button_stack.set_visible_child_name('exhale')

    def on_next_iter(self, timer):
        self._clean_circles()

    def on_stopped(self, timer):
        self._clean_circles()
        self.button_stack.set_visible_child_name('go')
        self.set_button_play_mode(False)

    def on_time_changed(self, timer, time_remaining):
        time_remaining = timer.time_remaining
        self.time_label.set_text("%02d∶%02d" % divmod(time_remaining // 10, 60))

    def _enlarge_circles(self):
        self.circle1.add_css_class("enlarge1")
        self.circle2.add_css_class("enlarge2")
        self.circle3.add_css_class("enlarge3")

    def _smallify_circles(self):
        self.circle1.add_css_class("smallify")
        self.circle2.add_css_class("smallify")
        self.circle3.add_css_class("smallify")

    def _clean_circles(self):
        self.circle1.remove_css_class("smallify")
        self.circle2.remove_css_class("smallify")
        self.circle3.remove_css_class("smallify")
        self.circle1.remove_css_class("enlarge1")
        self.circle2.remove_css_class("enlarge2")
        self.circle3.remove_css_class("enlarge3")

    def set_button_play_mode(self, is_play):
        if is_play:
            self.main_button.remove_css_class("suggested-action")
            self.main_button.add_css_class("playing")
        else:
            self.main_button.add_css_class("suggested-action")
            self.main_button.remove_css_class("playing")

    def toggle_breathing(self):
        if self.timer.time == 0:
            self.timer.start()
            self.set_button_play_mode(True)
        else:
            self.timer.stop()
