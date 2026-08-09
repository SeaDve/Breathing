# SPDX-FileCopyrightText: Copyright 2021 SeaDve
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gio, GLib

from breathing.timer import Timer


COLOR_SCHEMES = {
    "follow": Adw.ColorScheme.DEFAULT,
    "light": Adw.ColorScheme.FORCE_LIGHT,
    "dark": Adw.ColorScheme.FORCE_DARK,
}


@Gtk.Template(resource_path='/io/github/seadve/Breathing/ui/window.ui')
class BreathingWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'BreathingWindow'

    main_button = Gtk.Template.Child()
    button_stack = Gtk.Template.Child()
    circle1 = Gtk.Template.Child()
    circle2 = Gtk.Template.Child()
    circle3 = Gtk.Template.Child()
    time_label = Gtk.Template.Child()
    menu_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = Timer()
        self.settings = Gio.Settings.new("io.github.seadve.Breathing")
        self.style_manager = Adw.StyleManager.get_default()

        self._setup_style_action()
        self._setup_theme_selector()
        self.connect_signals()

    def _setup_style_action(self):
        saved = self.settings.get_string("style-variant")
        action = Gio.SimpleAction.new_stateful(
            "style-variant",
            GLib.VariantType("s"),
            GLib.Variant("s", saved),
        )
        action.connect("activate", self._on_style_variant_activate)
        self.add_action(action)
        self._apply_color_scheme(saved)

    def _apply_color_scheme(self, variant):
        self.style_manager.set_color_scheme(
            COLOR_SCHEMES.get(variant, Adw.ColorScheme.DEFAULT)
        )

    def _on_style_variant_activate(self, action, param):
        variant = param.get_string()
        action.set_state(param)
        self.settings.set_string("style-variant", variant)
        self._apply_color_scheme(variant)

    def _setup_theme_selector(self):
        follow_btn = Gtk.CheckButton(
            tooltip_text=_("Follow System Style"),
            hexpand=True,
            halign=Gtk.Align.CENTER,
            focus_on_click=False,
        )
        follow_btn.set_action_name("win.style-variant")
        follow_btn.set_action_target_value(GLib.Variant("s", "follow"))
        follow_btn.add_css_class("follow")

        light_btn = Gtk.CheckButton(
            tooltip_text=_("Light Style"),
            hexpand=True,
            halign=Gtk.Align.CENTER,
            focus_on_click=False,
            group=follow_btn,
        )
        light_btn.set_action_name("win.style-variant")
        light_btn.set_action_target_value(GLib.Variant("s", "light"))
        light_btn.add_css_class("light")

        dark_btn = Gtk.CheckButton(
            tooltip_text=_("Dark Style"),
            hexpand=True,
            halign=Gtk.Align.CENTER,
            focus_on_click=False,
            group=follow_btn,
        )
        dark_btn.set_action_name("win.style-variant")
        dark_btn.set_action_target_value(GLib.Variant("s", "dark"))
        dark_btn.add_css_class("dark")

        box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            hexpand=True,
        )
        box.add_css_class("themeselector")
        box.append(follow_btn)
        box.append(light_btn)
        box.append(dark_btn)

        self.menu_button.get_popover().add_child(box, "theme-selector")

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
            self.main_button.add_css_class("opaque")
        else:
            self.main_button.add_css_class("suggested-action")
            self.main_button.remove_css_class("opaque")

    def toggle_breathing(self):
        if self.timer.time == 0:
            self.timer.start()
            self.set_button_play_mode(True)
        else:
            self.timer.stop()
