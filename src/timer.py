# SPDX-FileCopyrightText: Copyright 2021 SeaDve
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GLib, GObject


class Timer(GObject.GObject):

    __gsignals__ = {
        'inhale': (GObject.SIGNAL_RUN_LAST, None, ()),
        'exhale': (GObject.SIGNAL_RUN_LAST, None, ()),
        'next-iter': (GObject.SIGNAL_RUN_LAST, None, ()),
        'stopped': (GObject.SIGNAL_RUN_LAST, None, ()),
    }

    time_remaining = GObject.Property(type=int)

    def __init__(self):
        super().__init__()
        self.time = 0

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
        self.stopped = False

    def stop(self):
        self.time_remaining = 0
        self.stopped = True
