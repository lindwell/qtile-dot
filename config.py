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

from typing import List  # noqa: F401
import os, subprocess
import iwlib
from plasma import Plasma

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook

colors = []
cache='/home/c13h21no3/.cache/wal/colors'
def load_colors(cache):
    with open(cache, 'r') as file:
        for i in range(8):
            colors.append(file.readline().strip())
    colors.append('#ffffff')
    lazy.reload()
load_colors(cache)

mod = "mod4"
terminal = "urxvt" 
rofi_alt_tab = "rofi -show window -show-icons"
rofi_run = "rofi -show run"
firefox = "firefox"
global_font = "agave regular Nerd Font Complete"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    #result of horrible attempts to make floating windows tile again
    
    #Key([mod], "space", lazy.toggle_focus_floating(), lazy.warp_cursor_here()),
    #Key([mod], "space", lazy.window.cmd_disable_floating()),
    Key([mod], "f", lazy.window.toggle_floating()),

    Key([mod, "shift"], "m", lazy.layout.maximize(), desc="Maximize window"),
    Key([mod], "m", lazy.layout.normalize()),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # application shortcuts
    Key([mod], "r", lazy.spawn(rofi_run),
        desc="Spawn a rofi run prompt"),
    Key([mod], "f", lazy.spawn(firefox), desc="run firefox"),
    Key(["mod1"], "Tab", lazy.spawn(rofi_alt_tab), desc="rofi Alt+Tab window switcher"),
    Key([mod], "e", lazy.spawn("thunar"), desc="run thunar"),

    #plasma layout keys
    Key([mod, "mod1"], "h", lazy.layout.integrate_left()),
    Key([mod, "mod1"], "j", lazy.layout.integrate_down()),
    Key([mod, "mod1"], "k", lazy.layout.integrate_up()),
    Key([mod, "mod1"], "l", lazy.layout.integrate_right()),
    Key([mod], "v", lazy.layout.mode_horizontal()),
    Key([mod], "d", lazy.layout.mode_vertical()),
    Key([mod, "shift"], "v", lazy.layout.mode_horizontal_split()),
    Key([mod, "shift"], "d", lazy.layout.mode_vertical_split()),
    Key([mod], "a", lazy.layout.grow_width(30)),
    Key([mod], "x", lazy.layout.grow_width(-30)),
    Key([mod, "shift"], "a", lazy.layout.grow_height(30)),
    Key([mod, "shift"], "x", lazy.layout.grow_height(-30)),
    Key([mod, "control"], "5", lazy.layout.size(500)),
    Key([mod, "control"], "8", lazy.layout.size(800)),
    Key([mod], "n", lazy.layout.reset_size()),

]

groups = [Group(i) for i in "123456"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.run([home])

def toggle_focus_floating():                                                                              
    '''Toggle focus between floating window and other windows in group'''
     
    @lazy.function
    def _toggle_focus_floating(qtile):
        group = qtile.current_group
        switch = 'non-float' if qtile.current_window.floating else 'float'
        logger.debug(f'toggle_focus_floating: switch = {switch}\t current_window: {qtile.current_window}')
        logger.debug(f'focus_history: {group.focus_history}')
         
         
        for win in reversed(group.focus_history):
            logger.debug(f'{win}: {win.floating}')
            if switch=='float' and win.floating:
                # win.focus(warp=False)
                group.focus(win)
                return
            if switch=='non-float' and not win.floating:
                # win.focus(warp=False)
                group.focus(win)
                return
    return _toggle_focus_floating

def init_layout_theme():
	return {"margin":		10,
		"border_width":		3,
		"border_focus":		colors[2],
		"border_normal":	colors[1],
		"border_focus":		colors[1],
		"border_single_width":	3,
		}

layout_theme = init_layout_theme()

layouts = [
    layout.Columns(**layout_theme),
    #layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    #layout.Stack(num_stacks=2),
    #layout.Tile(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Matrix(**layout_theme),
    layout.Floating(**layout_theme),
    #layout.Slice(**layout_theme),
    #Plasma(**layout_theme),
    # layout.MonadWide(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=global_font,
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
		widget.Sep(
			linewidth=0,
			padding=6,
			foreground=colors[2],
			background=colors[0]
		),
                widget.CurrentLayout(),
		widget.Sep(
			linewidth=0,
			padding=6,
			foreground=colors[2],
			background=colors[0]
		),
                widget.GroupBox(
			border=colors[2], 
			padding=3,
			rounded=True,
			borderwidth=3,
			this_current_screen_border=colors[2]
			),
                widget.WindowName(),
                widget.Prompt(),
                widget.Chord(
                    chords_colors={
                        'launch': (colors[2],colors[1]),
                    },
                    name_transform=lambda name: name.upper(),
                ),	
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
		widget.Wlan(),
		widget.Systray(),
		widget.Battery(),
                widget.QuickExit(),
            ],
            35,
	    background=colors[0],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='4kvideodownloader-bin'),
    Match(wm_class='mpv'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

autostart()
