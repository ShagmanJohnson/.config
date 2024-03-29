# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

mod = "mod4"
terminal = "alacritty"
myBrowser = "brave"
powerline1 = {
    "decorations": [
        PowerLineDecoration(path="rounded_left")
    ]
}
powerline2 = {
    "decorations": [
        PowerLineDecoration(path="zig_zag")
    ]
}
powerline3 = {
    "decorations": [
        PowerLineDecoration(path="rounded_right")
    ]
}

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Custom Keybindings 
    Key([mod], "b", lazy.spawn(myBrowser), desc="Launch Firefox"),
    Key([mod], "c", lazy.spawn("vscodium"), desc="Launch VsCodium"),
    Key([mod], "s", lazy.spawn("steam"), desc="Launch Steam"),
    Key([mod, "control"], "s", lazy.spawn("pavucontrol"), desc="Audio Controller"),
    Key([mod], "t", lazy.spawn("transmission"), desc="Launch Transmission"),
    Key([mod], "f", lazy.spawn("pcmanfm"), desc="File Manager"),
    Key([mod, "shift"], "b", lazy.spawn("chromium"), desc="Launch Chromium"),
    Key([mod], "d", lazy.spawn("flatpak run com.discordapp.Discord"), desc="Discord"),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

#groups = [Group(i) for i in "123456789"]
groups = [
Group('1', label="",                                      layout="Columns"),
Group('2', label="", matches=[Match(wm_class='steam')],   layout="Columns"),
Group('3', label="", matches=[Match(wm_class='discord')], layout="Max"),
Group('4', label="", matches=[Match(wm_class='vscodium')], layout="Columns"),
Group('5', label="", matches=[Match(wm_class='firefox')], layout="Max"),
Group('6', label="",                                      layout="Max"),
Group('7', label="", matches=[Match(wm_class='pcmanfm')], layout="Columns"),
Group('8', label="", matches=[Match(wm_class='pavucontrol')], layout="max"),
Group('9', label="", matches=[Match(wm_class='chromium')], layout="max"),

]
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_normal_stack=['#AE2012'],
        border_focus_stack=['#70e000'],
        border_focus = ['#70e000'],
        border_normal = ['#AE2012'],
        border_width=2,
        margin =0,
        num_columns=2
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
     layout.Matrix(
   border_normal_stack=['#AE2012'],
        border_focus_stack=['#70e000'],
        border_focus = ['#70e000'],
        border_normal = ['#AE2012'],
        border_width=2,
        margin =2,
     ),
     layout.MonadTall(
          border_normal_stack=['#AE2012'],
        border_focus_stack=['#70e000'],
        border_focus = ['#70e000'],
        border_normal = ['#AE2012'],
        border_width=4,
        margin =50,
     ),
     layout.MonadWide(),
    # layout.RatioTile(),
     layout.Tile(
        border_normal_stack=['#AE2012'],
        border_focus_stack=['#70e000'],
        border_focus = ['#70e000'],
        border_normal = ['#AE2012'],
        border_width=4,
        margin =20,),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

colors = [["#001219", "#001219"],
          ["#005F73", "#005F73"],
          ["#0A9396", "#0A9396"],
          ["#94D2BD", "#94D2BD"],
          ["#E9D8A6", "#E9D8A6"],
          ["#EE9B00", "#EE9B00"],
          ["#CA6702", "#CA6702"],
          ["#BB3E03", "#BB3E03"],
          ["#AE2012", "#AE2012"],
          ["#70e000", "#70e000"]]


widget_defaults = dict(
    font="QuinqueFive",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(
                    fontsize = 10,
                    background = colors [5],
                    foreground = colors [0],
                    **powerline1
                ),
                widget.GroupBox(
                    background = colors[0],
                    foreground = colors[3],
                    fontsize = 24,
                    active = colors [3],
                    inactive = colors [2],
                    **powerline2
                ),
                widget.Prompt(),
                widget.WindowName(
                    fontsize = 8,
                    background = colors [1],
                    foreground = colors [9],
                    **powerline1
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Clock(
                       background = colors[6],
                    foreground = colors[0],
                    format="%m-%d-%Y %a %I:%M %p",
                    fontsize =10,
                    ),
                widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "Updates: {updates} ",
                       foreground = colors[8], 
                       colour_have_updates = colors[8],
                       colour_no_updates = colors[4],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')},
                       padding = 5,
                       background = colors[0],
                       decorations=[
                           BorderDecoration(
                               colour = colors[9],
                               border_width = [0, 0, 2, 0],
                               padding_x = 5,
                               padding_y = None,
                           )
                       ],
                       ),

            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(
                    fontsize = 10,
                    background = colors [5],
                    foreground = colors [0],
                    **powerline1
                ),
                widget.GroupBox(
                 background = colors[0],
                    foreground = colors[3],
                    fontsize = 24,
                    active = colors [3],
                    inactive = colors [2],
                    **powerline2
                ),
                widget.Prompt(),
                widget.WindowName(
                     fontsize = 8,
                     background = colors[1],
                     foreground = colors[9],
                     **powerline1
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.NetGraph(
                    background = colors[0]
                ),
                widget.ThermalSensor(
                    fontsize = 10,
                    background = colors[0]
                ),
                widget.MemoryGraph(
                    background = colors[0]
                ),
                widget.CPUGraph(
                    type='line', line_width=2,
                    background = colors[0],
                    **powerline1

                    ),
                widget.Clock(
                    **powerline3,
                    background = colors[6],
                    foreground = colors[0],
                    format="%m-%d-%Y %a %I:%M %p",
                    fontsize =10
                    ),
                widget.QuickExit(
                    fontsize =24,
                    background = colors[4],
                    foreground = colors[8],
                default_text='', countdown_format='[{}]'
                ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
    ]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
