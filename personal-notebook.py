#!/usr/bin/env python3
#
# A script to run my notebook using the surf browser from Suckless
# surf is really ligthweight so I have plenty of memory to work with
# when I use it to manage my notebook tabs. It will always start in this
# directory so the context isn't shifting around on me, I can just open it
# anywhere.
#
# NOTE:
#	This is currently a piece of junk I didn't feel like working
# 	on too much at the time, so please forgive me for it's jank.
#
#	Ok, so I got frustrated enough to clean this up befere I
#	decided to use it. Hopefully I don't end up spending too much
#	extra time on it.

if __name__ != "__main__":
	exit("This is supposed to be an executable script numbnuts, don't try and import it please.")

# Standard Library Imports
import re, sys, os
import signal
from io import StringIO
from pathlib import Path
from threading import Event

try:
	from sh import jupyter
except ImportError:
	print("""
		Wow m8, is this me using this? Or someone else? You should probably
		go ahead and run "pip install -r requirements.txt"... Try not to
		make yourself look like an idiot okay? Sleep if you're tired.
		If you're someone else you can disregard this. I have a bad habit of
		overdoing shit.
	""")
	sys.exit(1)

try:
	from sh import chromium_browser
except ImportError:
	print("Error: you need chromium-browser to run this program.")
	#print("Error: you need surf from suckless tools to run this program.")
	sys.exit(1)


surfer = None
joy = None
joy_started = Event()
joy_press = re.compile(r'http://[\S]+')
joy_mill = re.compile(r'\d+(?=\/.*)')
joy_key = ""
joy_keys = 0
joy_port = ""

def joy_con(data):
	# For some reason this is needed otherwise everythign else fails
	global joy_keys, joy_mill, joy_key, joy_port, joy_press, joy_started
	print(data.rstrip("\n")); # print out everything cleaning newlines

	pressed = joy_press.search(data)
	if pressed != None:
		joy_key = pressed.group(0)
		joy_port = joy_mill.search(joy_key).group(0)

		joy_keys =+ 1
		if joy_keys >= 1:
			joy_started.set()

def exit_handler(signal, frame):
	if joy is not None:
		joy.kill()
	if surfer is not None:
		surfer.kill()


# resolve the actual file that's executing using symlink tracing.
script = Path(__file__)
if script.is_symlink(): script = script.resolve()
os.chdir(str(script.parent)) # just to be save.

# Register the signal handlers so if our user is in a terminal they can close
# everything from there.
signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGINT, exit_handler)

# Runs a private notebook server in the directory this script is in.
joy = jupyter.notebook(
	"--no-browser",
	"--notebook-dir", str(script.parent),

	_bg=True, _out=joy_con, _err=joy_con
)
joy_started.wait() # wait for initialization to finish

# Start the browser session.
surfer = chromium_browser(
	# loads a new chromium instance so this doesn't open in a pre-existing
	# process and terminate early.
	"--temp-profile",
	# forces dark mode borders and such. Just in case they appear somehow.
	"--force-dark-mode",
	# removes the window borders and url bar.
	"--app="+joy_key
)

# When the browser is closed, close down the server
jupyter.notebook.stop(joy_port)
