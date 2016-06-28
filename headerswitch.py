#!/usr/bin/env python
#
# Copyright (C) 2016 Martin Willi
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See <http://www.fsf.org/copyleft/gpl.txt>.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

import os
from gi.repository import GObject, Gtk, Gio, Gedit, GtkSource

class HeaderSwitchWindow(GObject.Object, Gedit.WindowActivatable):
	__gtype_name__ = 'HeaderSwitchWindow'
	window = GObject.property(type=Gedit.Window)
	extpairs = [
		[ '.c', '.h' ]
	]

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		action = Gio.SimpleAction(name="headerswitch")
		action.connect('activate', self.on_switch)
		self.window.add_action(action)

	def do_deactivate(self):
		self.window.remove_action("headerswitch")

	def do_update_state(self):
		pass

	def do_switch(self, path):
		for doc in self.window.get_documents():
			loc = doc.get_location()
			if loc and path == loc.get_path():
				tab = Gedit.Tab.get_from_document(doc)
				if tab:
					self.window.set_active_tab(tab)
					return
		self.window.create_tab_from_location(Gio.file_new_for_path(path),
											 None, 0, 0, True, True)

	def on_switch(self, action, parameter, user_data=None):
		doc = self.window.get_active_document()
		if doc:
			loc = doc.get_location()
			if loc:
				path = loc.get_path()
				if path:
					root, ext = os.path.splitext(path)
					if ext:
						for pair in self.extpairs:
							if ext == pair[0]:
								self.do_switch(root + pair[1])
							if ext == pair[1]:
								self.do_switch(root + pair[0])

class HeaderSwitchApp(GObject.Object, Gedit.AppActivatable):
	__gtype_name__ = 'HeaderSwitchApp'
	app = GObject.property(type=Gedit.App)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		self.app.add_accelerator("<Ctrl>R", "win.headerswitch", None)

		self.menu_ext = self.extend_menu("tools-section")
		item = Gio.MenuItem.new("Switch .c/.h", "win.headerswitch")
		self.menu_ext.append_menu_item(item)

	def do_deactivate(self):
		self.app.remove_accelerator("win.headerswitch", None)
		self.menu_ext = None
