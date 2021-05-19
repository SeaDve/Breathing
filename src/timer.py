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

from gi.repository import GLib, GObject


class Timer(GObject.GObject):

    __gsignals__ = {
        'inhale': (GObject.SIGNAL_RUN_LAST, None, ()),
        'exhale': (GObject.SIGNAL_RUN_LAST, None, ()),
        'next-iter': (GObject.SIGNAL_RUN_LAST, None, ()),
        'stopped': (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    time_remaining = GObject.Property(type=int, flags=GObject.ParamFlags.READWRITE)

    def __init__(self):
        super().__init__()

    def _refresh_time(self):
        if self.iterations >= 10 or self.stopped:
            self.emit('stopped')
            self.time = 0
            return False
        if 1 <= self.time <= 20:
            self.emit('inhale')
        elif 40 <= self.time <= 100:
            self.emit('exhale')
        elif self.time == 110:
            self.emit('next-iter')
            self.time = 0
            self.iterations += 1
        self.time += 1
        self.time_remaining -= 1
        return True

    def start(self):
        GLib.timeout_add(100, self._refresh_time, priority=GLib.PRIORITY_LOW)
        self.time_remaining = 1105
        self.iterations = 0
        self.time = 0
        self.stopped = False

    def stop(self):
        self.time_remaining = 0
        self.stopped = True
