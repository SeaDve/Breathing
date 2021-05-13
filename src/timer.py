# timer.py
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

from gi.repository import GLib


class Timer:
    def __init__(self, stack, win):
        self.stack = stack
        self.win = win
        self.time = 0

    def _refresh_time(self):
        if self.iterations > 100 or self.cancelled:
            self.stack.set_visible_child_name("go")
            self.win.set_button_play_mode(False)
            self.win.clean_circles()
            self.time = 0
            return False

        if 1 <= self.time <= 20:
            self.win.enlarge_circles()
            self.stack.set_visible_child_name("inhale")
        elif 40 <= self.time <= 100:
            self.win.smallify_circles()
            self.stack.set_visible_child_name("exhale")
        elif self.time == 110:
            self.win.clean_circles()
            self.time = 0
            self.iterations += 1
        self.time += 1
        return True

    def start(self):
        GLib.timeout_add(100, self._refresh_time, priority=GLib.PRIORITY_LOW)
        self.win.set_button_play_mode(True)
        self.cancelled = False
        self.iterations = 0

    def cancel(self):
        self.cancelled = True
