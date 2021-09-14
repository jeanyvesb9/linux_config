# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

from plasma import Plasma

mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"                             # My terminal of choice

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "Return",
             #lazy.spawn("dmenu_run -p 'Run: '"),
             #lazy.spawn("rofi -show drun -config ~/.config/rofi/themes/dt-dmenu.rasi -display-drun \"Run: \" -drun-display-format \"{name}\""),
             lazy.spawn("rofi -show drun -font 'JetBrainsMono Nerd Font 12'"),
             desc='Run Launcher'
             ),
         Key([mod], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "control", "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         ### Switch focus to specific monitor (out of three)
         Key([mod], "q",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "w",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         #Key([mod], "e",
             #lazy.to_screen(2),
             #desc='Keyboard focus to monitor 3'
             #),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Window controls
         Key([mod], "h",
             lazy.layout.left(),
             desc='Move focus left in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod], "l",
             lazy.layout.right(),
             desc='Move focus right in current stack pane'
             ),
         Key([mod, "shift"], "h",
             lazy.layout.shuffle_left(),
             lazy.layout.move_left(),
             desc='Move windows left in current stack'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.move_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.move_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod, "shift"], "l",
             lazy.layout.shuffle_right(),
             lazy.layout.move_right(),
             desc='Move windows right in current stack'
             ),
         Key([mod, "control", "shift"], "h",
             lazy.layout.integrate_left(),
             desc='Flip left'
             ),
         Key([mod, "control", "shift"], "j",
             lazy.layout.integrate_down(),
             desc='Flip down'
             ),
         Key([mod, "control", "shift"], "k",
             lazy.layout.integrate_up(),
             desc='Flip up'
             ),
         Key([mod, "control", "shift"], "l",
             lazy.layout.integrate_right(),
             desc='Flip right'
             ),
         Key([mod], "m",
             lazy.layout.shrink(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "i",
             lazy.layout.grow(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod, "control"], "h",
             lazy.layout.grow_width(-30),
             desc='Grow window left'
             ),
         Key([mod, "control"], "j",
             lazy.layout.grow_height(-30),
             desc='Grow window down'
             ),
         Key([mod, "control"], "k",
             lazy.layout.grow_height(30),
             desc='Grow window up'
             ),
         Key([mod, "control"], "l",
             lazy.layout.grow_width(30),
             desc='Grow window right'
             ),
         Key([mod], "r",
             lazy.layout.reset(),
             lazy.layout.reset_size(),
             desc='Reset window size ratios'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='Normalize window size ratios'
             ),
         Key([mod], "o",
             lazy.layout.maximize(),
             desc='Toggle window between minimum and maximum sizes'
             ),
         Key([mod], "d",
             lazy.layout.mode_horizontal(),
             desc='Toggle mode horizontal'
             ),
         Key([mod], "f",
             lazy.layout.mode_vertical(),
             desc='Toggle mode vertical'
             ),
         Key([mod, "shift"], "d",
             lazy.layout.mode_horizontal_split(),
             desc='Toggle mode horizontal split'
             ),
         Key([mod, "shift"], "f",
             lazy.layout.mode_vertical_split(),
             desc='Toggle mode vertical split'
             ),
         Key([mod], "f",
             lazy.window.toggle_floating(),
             desc='Toggle floating'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_fullscreen(),
             desc='Toggle fullscreen'
             ),
         Key([mod, "shift"], "Tab",
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
         KeyChord([mod], "p", [
             Key([], "e",
                 lazy.spawn("./dmscripts/dmconf"),
                 desc='Choose a config file to edit'
                 ),
             Key([], "i",
                 lazy.spawn("./dmscripts/dmscrot"),
                 desc='Take screenshots via dmenu'
                 ),
             Key([], "k",
                 lazy.spawn("./dmscripts/dmkill"),
                 desc='Kill processes via dmenu'
                 ),
             Key([], "l",
                 lazy.spawn("./dmscripts/dmlogout"),
                 desc='A logout menu'
                 ),
         ]),
         Key([mod], "Escape",
             lazy.spawn("kill -s USR1 $(pidof deadd-notification-center)"),
             desc='Notification center'
             ),
]

group_names = [("I", {'layout': 'monadtall'}),
               ("II", {'layout': 'monadtall'}),
               ("III", {'layout': 'monadtall'}),
               ("IV", {'layout': 'monadtall'}),
               ("V", {'layout': 'monadtall'}),
               ("VI", {'layout': 'monadtall'}),
               ("VII", {'layout': 'monadtall'}),
               ("VIII", {'layout': 'monadtall'}),
               ("IX", {'layout': 'monadtall'}),
               ("M", {'layout': 'monadtall'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names[:9], 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group
    keys.append(Key([mod, "control", "shift"], str(i), lazy.window.togroup(name), lazy.group[name].toscreen())) # Send current window to another group

#Special groups setup:
# NONE (Mining group is not bound to keyboard keys)

layout_theme = {"border_width": 2,
                "margin": 6,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    Plasma(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    #layout.TreeTab(
    #     font = "Ubuntu",
    #     fontsize = 10,
    #     sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
    #     section_fontsize = 10,
    #     border_width = 2,
    #     bg_color = "1c1f24",
    #     active_bg = "c678dd",
    #     active_fg = "000000",
    #     inactive_bg = "a9a1e1",
    #     inactive_fg = "1c1f24",
    #     padding_left = 0,
    #     padding_x = 0,
    #     padding_y = 5,
    #     section_top = 10,
    #     section_bottom = 20,
    #     level_shift = 8,
    #     vspace = 3,
    #     panel_width = 200
    #     ),
    layout.Floating(**layout_theme)
]

colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # backbround for inactive screens

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="JetBrains Mono Nerd Font Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.TextBox(
                       text = '◥',
                       background = colors[0],
                       foreground = colors[4], #"#81A1C1",
                       padding = -2,
                       font= "Fira Code",
                       fontsize = 50
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[2],
                       padding = 0,
                       fontsize = 28,
                       mouse_callbacks = {'button1': lambda: qtile.cmd_spawn(myterm)}
                       ),
              widget.TextBox(
                       text = '◣',
                       background = colors[0],
                       foreground = colors[4], #"#81A1C1",
                       padding = -2,
                       font = "Fira Code",
                       fontsize = 50
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 1,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 9,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[7],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = colors[3],
                       background = colors[1]
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 10,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.TextBox(
                       text = '◥',
                       background = colors[0],
                       foreground = colors[4],
                       padding = -2,
                       font = "Fira Code",
                       fontsize = 50
                       ),
             widget.Net(
                       interface = "bond0",
                       format = '{down} ↓↑ {up}',
                       foreground = colors[2],
                       background = colors[4],
                       padding = 5
                       ),
             widget.TextBox(
                       text='◢',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -2,
                       font = "Fira Code",
                       fontsize = 50
                       ),
             widget.TextBox(
                       text = "💻",
                       padding = 2,
                       foreground = colors[4],
                       background = colors[5],
                       fontsize = 14
                       ),
             widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "{updates} Updates",
                       foreground = colors[2],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       background = colors[5]
                       ),
             widget.TextBox(
                       text = '◢',
                       background = colors[5],
                       foreground = colors[4],
                       padding = -2,
                       font = "Fira Code",
                       fontsize = 50
                       ),
             widget.TextBox(
                       text = "💾",
                       foreground = colors[2],
                       background = colors[4],
                       padding = 0,
                       fontsize = 14
                       ),
             widget.Memory(
                       foreground = colors[2],
                       background = colors[4],
                       measure_mem = "g",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e gotop')},
                       padding = 5
                       ),
             widget.TextBox(
                       text = '◢',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -2,
                       font = "Fira Code",
                       fontsize = 50
                       ),
             widget.TextBox(
                      text = " 🎧 Vol:",
                       foreground = colors[2],
                       background = colors[5],
                       padding = 0
                       ),
             widget.Volume(
                       foreground = colors[2],
                       background = colors[5],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '◢',
                       background = colors[5],
                       foreground = colors[4],
                       padding = -2,
                       font = "Fira Code",
                       fontsize = 50
                       ),
             widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[4],
                       padding = 0,
                       scale = 0.7
                       ),
             widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[4],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '◢',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -2,
                       font = "Fira Code",
                       fontsize = 50
                       ),
              widget.Clock(
                       foreground = colors[2],
                       background = colors[5],
                       format = "📅 %Y-%m-%d, %H:%M:%S ",
                       timezone = "America/Argentina/Buenos_Aires",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e cal')}
                       ),
              widget.TextBox(
                      text= '◣',
                      background = colors[0],
                      foreground = colors[5],
                      padding = -2,
                      font = "Fira Code",
                      fontsize = 50
                      ),
              widget.Systray(
                      background = colors[0],
                      padding = 0
                      ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    #del widgets_screen1[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20))]
            #Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),  # tastyworks exit box
    Match(title='Qalculate!'),  # qalculate-gtk
    Match(wm_class='kdenlive'),  # kdenlive
    Match(wm_class='pinentry-gtk-2'),  # GPG key password entry
    Match(title='Volume Control'),
    Match(title='Bluetooth Devices'),
    Match(title='CopyQ'),
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
