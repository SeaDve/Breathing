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

from gi.repository import Gtk, Adw, GLib


@Gtk.Template(resource_path='/io/github/seadve/Breathing/ui/window.ui')
class BreathingWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BreathingWindow'

    main_button = Gtk.Template.Child()
    button_stack = Gtk.Template.Child()
    circle1 = Gtk.Template.Child()
    circle2 = Gtk.Template.Child()
    circle3 = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = Timer(self.button_stack, self)

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

    @Gtk.Template.Callback()
    def on_main_button_clicked(self, button):
        if self.timer.time == 0:
            self.timer.start()
        else:
            self.timer.cancel()

    @Gtk.Template.Callback()
    def on_dark_mode_button_clicked(self, button):
        if button.get_icon_name() == "light-mode-symbolic":
            button.set_icon_name("dark-mode-symbolic")
            self.dark_mode_circle.get_style_context().add_class("dark-mode")
        else:
            button.set_icon_name("light-mode-symbolic")
            self.dark_mode_circle.get_style_context().remove_class("dark-mode")

        # TODO implement dark mode


class Timer:
    def __init__(self, stack, win):
        self.stack = stack
        self.win = win
        self.time = 0

    def _refresh_time(self):
        if self.iterations > 10 or self.cancelled:
            self.stack.set_visible_child_name("go")
            self.win.set_button_play_mode(False)
            self.win.clean_circles()
            self.time = 0
            return False

        if 1 <= self.time <= 2:
            self.win.enlarge_circles()
            self.stack.set_visible_child_name("inhale")
        elif 4 <= self.time <= 10:
            self.win.smallify_circles()
            self.stack.set_visible_child_name("exhale")
        elif self.time == 11:
            self.win.clean_circles()
            self.time = 0
            self.iterations += 1
        self.time += 1
        return True

    def start(self):
        GLib.timeout_add_seconds(1, self._refresh_time, priority=GLib.PRIORITY_LOW)
        self.win.set_button_play_mode(True)
        self.cancelled = False
        self.iterations = 0

    def cancel(self):
        self.cancelled = True
