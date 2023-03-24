#!/usr/bin/env python9
# -*- coding:UTF-8 -*-
"""
    This file will control some options of the gmoccapy plasma screen
    and demonstrats at the same time the possibilities you have introducing
    your own handler files and functions to that screen, showing the
    possibilities to modify the layout and behavior

    Copyright 2013 Norbert Schechner
    nieson@web.de

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""

import hal_glib                           # needed to make our own hal pins
import hal                                # needed to make our own hal pins
from gladevcp.persistence import IniFile  # we use this one to save the states of the widgets on shut down and restart
from gladevcp.persistence import widget_defaults
from gladevcp.persistence import select_widgets
import gtk
from gmoccapy import preferences
from gmoccapy import getiniinfo

class PlasmaClass:

    def __init__(self, halcomp, builder, useropts):
        self.builder = builder
        self.halcomp = halcomp
        self.defaults = { IniFile.vars : { "pierce_hghtval"      : 3.0 ,
                                           "pierce_hghtmax"      : 15.0 ,
                                           "pierce_hghtmin"      : 1.0  ,
                                           "pierce_hghtincr"     : 0.5  ,

					                       "jump_hghtval"        : 0.0 ,
                                           "jump_hghtmax"        : 15.0 ,
                                           "jump_hghtmin"        : 0.0  ,
                                           "jump_hghtincr"       : 0.5  ,

					                       "cut_hghtval"         : 6.0 ,
                                           "cut_hghtmax"         : 15.0 ,
                                           "cut_hghtmin"         : 0.0  ,
                                           "cut_hghtincr"        : 0.5  ,

					                       "pierce_delval"       : 0.0 ,
                                           "pierce_delmax"       : 5.0 ,
                                           "pierce_delmin"       : 0.0  ,
                                           "pierce_delincr"      : 0.1  ,

					                       "safe_zval"           : 30.0 ,
                                           "safe_zmax"           : 100.0 ,
                                           "safe_zmin"           : 0.0  ,
                                           "safe_zincr"          : 5.0  ,

					                       "z_speedval"          : 750.0 ,
                                           "z_speedmax"          : 1000.0 ,
                                           "z_speedmin"          : 100.0  ,
                                           "z_speedincr"         : 50.0  ,

					                       "stop_delval"         : 13.0 ,
                                           "stop_delmax"         : 20.0 ,
                                           "stop_delmin"         : 0.0  ,
                                           "stop_delincr"        : 1.0  ,

					                       "cor_velval"         : 20.0 ,
                                           "cor_velmax"         : 100.0 ,
                                           "cor_velmin"         : 0.0  ,
                                           "cor_velincr"        : 5.0  ,

					                       "vel_tolval"         : 90.0 ,
                                           "vel_tolmax"         : 100.0 ,
                                           "vel_tolmin"         : 0.0  ,
                                           "vel_tolincr"        : 5.0  ,
                                           
                                           #"cutmode_val"         : none ,
                                           #"cutmode_plasma"      : Plasma ,
                                           #"cutmode_oxygen"      : Oxygen ,
                                           

                                           
                                         },
                          IniFile.widgets: widget_defaults(select_widgets([self.builder.get_object("hal-btn-THC"),
                                                                          ], hal_only = True, output_only = True)),
                        }

        get_ini_info = getiniinfo.GetIniInfo()
        prefs = preferences.preferences(get_ini_info.get_preference_file_path())
        theme_name = prefs.getpref("gtk_theme", "Follow System Theme", str)
        if theme_name == "Follow System Theme":
            theme_name = gtk.settings_get_default().get_property("gtk-theme-name")
        gtk.settings_get_default().set_string_property("gtk-theme-name", theme_name, "")

        self.ini_filename = __name__ + ".var"
        self.ini = IniFile(self.ini_filename, self.defaults, self.builder)
        self.ini.restore_state(self)

# lets make our pins
        self.halpin_pierce_hght = hal_glib.GPin(halcomp.newpin("prc-hght", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_jump_hght = hal_glib.GPin(halcomp.newpin("jump", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_cut_hght = hal_glib.GPin(halcomp.newpin("cut-hght", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_pierce_del = hal_glib.GPin(halcomp.newpin("prc-del", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_safe_z = hal_glib.GPin(halcomp.newpin("safe-z", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_z_speed = hal_glib.GPin(halcomp.newpin("z-speed", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_stop_del = hal_glib.GPin(halcomp.newpin("stop-del", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_cor_vel = hal_glib.GPin(halcomp.newpin("cor-vel", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_vel_tol = hal_glib.GPin(halcomp.newpin("vel-tol", hal.HAL_FLOAT, hal.HAL_OUT))
	self.halpin_cutmode = hal_glib.GPin(halcomp.newpin("cutmode", hal.HAL_S32, hal.HAL_IN))
	
     
# get all widgets and connect them
        self.lbl_pierce_hght = self.builder.get_object("lbl_pierce_hght")
	self.lbl_jump_hght = self.builder.get_object("lbl_jump_hght")
	self.lbl_cut_hght = self.builder.get_object("lbl_cut_hght")
	self.lbl_pierce_del = self.builder.get_object("lbl_pierce_del")
	self.lbl_safe_z = self.builder.get_object("lbl_safe_z")
	self.lbl_z_speed = self.builder.get_object("lbl_z_speed")
	self.lbl_stop_del = self.builder.get_object("lbl_stop_del")
	self.lbl_cor_vel = self.builder.get_object("lbl_cor_vel")
	self.lbl_vel_tol = self.builder.get_object("lbl_vel_tol")
	

#pierce_hght buttons
	self.btn_pierce_hght_plus = self.builder.get_object("btn_pierce_hght_plus")
        self.btn_pierce_hght_plus.connect("pressed", self.btn_pierce_hght_pressed, 1)

        self.btn_pierce_hght_minus = self.builder.get_object("btn_pierce_hght_minus")
        self.btn_pierce_hght_minus.connect("pressed", self.btn_pierce_hght_pressed, -1)

#jump_hght buttons
	self.btn_jump_hght_plus = self.builder.get_object("btn_jump_hght_plus")
        self.btn_jump_hght_plus.connect("pressed", self.btn_jump_hght_pressed, 1)

        self.btn_jump_hght_minus = self.builder.get_object("btn_jump_hght_minus")
        self.btn_jump_hght_minus.connect("pressed", self.btn_jump_hght_pressed, -1)

#cut_hght buttons
	self.btn_cut_hght_plus = self.builder.get_object("btn_cut_hght_plus")
        self.btn_cut_hght_plus.connect("pressed", self.btn_cut_hght_pressed, 1)

        self.btn_cut_hght_minus = self.builder.get_object("btn_cut_hght_minus")
        self.btn_cut_hght_minus.connect("pressed", self.btn_cut_hght_pressed, -1)

#pierce_del buttons
	self.btn_pierce_del_plus = self.builder.get_object("btn_pierce_del_plus")
        self.btn_pierce_del_plus.connect("pressed", self.btn_pierce_del_pressed, 1)

        self.btn_pierce_del_minus = self.builder.get_object("btn_pierce_del_minus")
        self.btn_pierce_del_minus.connect("pressed", self.btn_pierce_del_pressed, -1)

#safe_z buttons
	self.btn_safe_z_plus = self.builder.get_object("btn_safe_z_plus")
        self.btn_safe_z_plus.connect("pressed", self.btn_safe_z_pressed, 1)

        self.btn_safe_z_minus = self.builder.get_object("btn_safe_z_minus")
        self.btn_safe_z_minus.connect("pressed", self.btn_safe_z_pressed, -1)

#z_speed buttons
	self.btn_z_speed_plus = self.builder.get_object("btn_z_speed_plus")
        self.btn_z_speed_plus.connect("pressed", self.btn_z_speed_pressed, 1)

        self.btn_z_speed_minus = self.builder.get_object("btn_z_speed_minus")
        self.btn_z_speed_minus.connect("pressed", self.btn_z_speed_pressed, -1)

#stop_del buttons
	self.btn_stop_del_plus = self.builder.get_object("btn_stop_del_plus")
        self.btn_stop_del_plus.connect("pressed", self.btn_stop_del_pressed, 1)

        self.btn_stop_del_minus = self.builder.get_object("btn_stop_del_minus")
        self.btn_stop_del_minus.connect("pressed", self.btn_stop_del_pressed, -1)

#cor_vel buttons
	self.btn_cor_vel_plus = self.builder.get_object("btn_cor_vel_plus")
        self.btn_cor_vel_plus.connect("pressed", self.btn_cor_vel_pressed, 1)

        self.btn_cor_vel_minus = self.builder.get_object("btn_cor_vel_minus")
        self.btn_cor_vel_minus.connect("pressed", self.btn_cor_vel_pressed, -1)

#vel_tol buttons
	self.btn_vel_tol_plus = self.builder.get_object("btn_vel_tol_plus")
        self.btn_vel_tol_plus.connect("pressed", self.btn_vel_tol_pressed, 1)

        self.btn_vel_tol_minus = self.builder.get_object("btn_vel_tol_minus")
        self.btn_vel_tol_minus.connect("pressed", self.btn_vel_tol_pressed, -1)

#adj_pierce_hght
        self.adj_pierce_hght = self.builder.get_object("adj_pierce_hght")
        self.adj_pierce_hght.connect("value_changed", self.adj_pierce_hght_changed)

        self.adj_pierce_hght.upper = self.pierce_hghtmax
        self.adj_pierce_hght.lower = self.pierce_hghtmin
        self.adj_pierce_hght.set_value(self.pierce_hghtval)

#adj_jump_height
	self.adj_jump_height = self.builder.get_object("adj_jump_height")
        self.adj_jump_height.connect("value_changed", self.adj_jump_height_changed)

        self.adj_jump_height.upper = self.jump_hghtmax
        self.adj_jump_height.lower = self.jump_hghtmin
        self.adj_jump_height.set_value(self.jump_hghtval)

#adj_cut_height
	self.adj_cut_hght = self.builder.get_object("adj_cut_hght")
        self.adj_cut_hght.connect("value_changed", self.adj_cut_hght_changed)

        self.adj_cut_hght.upper = self.cut_hghtmax
        self.adj_cut_hght.lower = self.cut_hghtmin
        self.adj_cut_hght.set_value(self.cut_hghtval)

#adj_cut_height
	self.adj_pierce_del = self.builder.get_object("adj_pierce_del")
        self.adj_pierce_del.connect("value_changed", self.adj_pierce_del_changed)

        self.adj_pierce_del.upper = self.pierce_delmax
        self.adj_pierce_del.lower = self.pierce_delmin
        self.adj_pierce_del.set_value(self.pierce_delval)

#adj_safe_z
	self.adj_safe_z = self.builder.get_object("adj_safe_z")
        self.adj_safe_z.connect("value_changed", self.adj_safe_z_changed)

        self.adj_safe_z.upper = self.safe_zmax
        self.adj_safe_z.lower = self.safe_zmin
        self.adj_safe_z.set_value(self.safe_zval)

#adj_z_speed
	self.adj_z_speed = self.builder.get_object("adj_z_speed")
        self.adj_z_speed.connect("value_changed", self.adj_z_speed_changed)

        self.adj_z_speed.upper = self.z_speedmax
        self.adj_z_speed.lower = self.z_speedmin
        self.adj_z_speed.set_value(self.z_speedval)

#adj_stop_del
	self.adj_stop_del = self.builder.get_object("adj_stop_del")
        self.adj_stop_del.connect("value_changed", self.adj_stop_del_changed)

        self.adj_stop_del.upper = self.stop_delmax
        self.adj_stop_del.lower = self.stop_delmin
        self.adj_stop_del.set_value(self.stop_delval)

#adj_cor_vel
	self.adj_cor_vel = self.builder.get_object("adj_cor_vel")
        self.adj_cor_vel.connect("value_changed", self.adj_cor_vel_changed)

        self.adj_cor_vel.upper = self.cor_velmax
        self.adj_cor_vel.lower = self.cor_velmin
        self.adj_cor_vel.set_value(self.cor_velval)

#adj_vel_tol
	self.adj_vel_tol = self.builder.get_object("adj_vel_tol")
        self.adj_vel_tol.connect("value_changed", self.adj_vel_tol_changed)

        self.adj_vel_tol.upper = self.vel_tolmax
        self.adj_vel_tol.lower = self.vel_tolmin
        self.adj_vel_tol.set_value(self.vel_tolval)

    def btn_pierce_hght_pressed(self, widget, dir):
        increment = self.pierce_hghtincr * dir
        self.pierce_hghtval = self.adj_pierce_hght.get_value() + increment
        self.adj_pierce_hght.set_value(self.pierce_hghtval)

    def btn_jump_hght_pressed(self, widget, dir):
        increment = self.jump_hghtincr * dir
        self.jump_hghtval = self.adj_jump_height.get_value() + increment
        self.adj_jump_height.set_value(self.jump_hghtval)
        
    def btn_cut_hght_pressed(self, widget, dir):
        increment = self.cut_hghtincr * dir
        self.cut_hghtval = self.adj_cut_hght.get_value() + increment
        self.adj_cut_hght.set_value(self.cut_hghtval)

    def btn_pierce_del_pressed(self, widget, dir):
        increment = self.pierce_delincr * dir
        self.pierce_delval = self.adj_pierce_del.get_value() + increment
        self.adj_pierce_del.set_value(self.pierce_delval)

    def btn_safe_z_pressed(self, widget, dir):
        increment = self.safe_zincr * dir
        self.safe_zval = self.adj_safe_z.get_value() + increment
        self.adj_safe_z.set_value(self.safe_zval)

    def btn_z_speed_pressed(self, widget, dir):
        increment = self.z_speedincr * dir
        self.z_speedval = self.adj_z_speed.get_value() + increment
        self.adj_z_speed.set_value(self.z_speedval)

    def btn_stop_del_pressed(self, widget, dir):
        increment = self.stop_delincr * dir
        self.stop_delval = self.adj_stop_del.get_value() + increment
        self.adj_stop_del.set_value(self.stop_delval)

    def btn_cor_vel_pressed(self, widget, dir):
        increment = self.cor_velincr * dir
        self.cor_velval = self.adj_cor_vel.get_value() + increment
        self.adj_cor_vel.set_value(self.cor_velval)

    def btn_vel_tol_pressed(self, widget, dir):
        increment = self.vel_tolincr * dir
        self.vel_tolval = self.adj_vel_tol.get_value() + increment
        self.adj_vel_tol.set_value(self.vel_tolval)
        
    def plasma_mode(self, widget, data = None):
        if self.halpin_plasma == (False):
			self.lbl_cutmode = 'Plasma mode'
		#elif self.halpin_oxygen == 1:
		#	self.lbl_cutmode = 'OYGEN mode'
		#else:
		#	self.lbl_cutmode = 'Nomode'
			
        
        




    def adj_pierce_hght_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_pierce_hght_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_pierce_hght_minus.set_sensitive(False)
        else:
            self.btn_pierce_hght_plus.set_sensitive(True)
            self.btn_pierce_hght_minus.set_sensitive(True)
        self.halcomp["prc-hght"] = widget.get_value()
        self.lbl_pierce_hght.set_label("%.1f" % (widget.get_value()))

    def adj_jump_height_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_jump_hght_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_jump_hght_minus.set_sensitive(False)
        else:
            self.btn_jump_hght_plus.set_sensitive(True)
            self.btn_jump_hght_minus.set_sensitive(True)
        self.halcomp["jump"] = widget.get_value()
        self.lbl_jump_hght.set_label("%.1f" % (widget.get_value()))

    def adj_cut_hght_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_cut_hght_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_cut_hght_minus.set_sensitive(False)
        else:
            self.btn_cut_hght_plus.set_sensitive(True)
            self.btn_cut_hght_minus.set_sensitive(True)
        self.halcomp["cut-hght"] = widget.get_value()
        self.lbl_cut_hght.set_label("%.1f" % (widget.get_value()))

    def adj_pierce_del_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_pierce_del_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_pierce_del_minus.set_sensitive(False)
        else:
            self.btn_pierce_del_plus.set_sensitive(True)
            self.btn_pierce_del_minus.set_sensitive(True)
        self.halcomp["prc-del"] = widget.get_value()
        self.lbl_pierce_del.set_label("%.1f" % (widget.get_value()))

    def adj_safe_z_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_safe_z_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_safe_z_minus.set_sensitive(False)
        else:
            self.btn_safe_z_plus.set_sensitive(True)
            self.btn_safe_z_minus.set_sensitive(True)
        self.halcomp["safe-z"] = widget.get_value()
        self.lbl_safe_z.set_label("%.1f" % (widget.get_value()))

    def adj_z_speed_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_z_speed_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_z_speed_minus.set_sensitive(False)
        else:
            self.btn_z_speed_plus.set_sensitive(True)
            self.btn_z_speed_minus.set_sensitive(True)
        self.halcomp["z-speed"] = widget.get_value()
        self.lbl_z_speed.set_label("%.1f" % (widget.get_value()))

    def adj_stop_del_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_stop_del_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_stop_del_minus.set_sensitive(False)
        else:
            self.btn_stop_del_plus.set_sensitive(True)
            self.btn_stop_del_minus.set_sensitive(True)
        self.halcomp["stop-del"] = widget.get_value()
        self.lbl_stop_del.set_label("%.1f" % (widget.get_value()))

    def adj_cor_vel_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_cor_vel_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_cor_vel_minus.set_sensitive(False)
        else:
            self.btn_cor_vel_plus.set_sensitive(True)
            self.btn_cor_vel_minus.set_sensitive(True)
        self.halcomp["cor-vel"] = widget.get_value()
        self.lbl_cor_vel.set_label("%.1f" % (widget.get_value()))

    def adj_vel_tol_changed(self, widget, data = None):
        if widget.get_value() >= widget.upper:
            self.btn_vel_tol_plus.set_sensitive(False)
        elif widget.get_value() <= widget.lower:
            self.btn_vel_tol_minus.set_sensitive(False)
        else:
            self.btn_vel_tol_plus.set_sensitive(True)
            self.btn_vel_tol_minus.set_sensitive(True)
        self.halcomp["vel-tol"] = widget.get_value()
        self.lbl_vel_tol.set_label("%.1f" % (widget.get_value()))



def get_handlers(halcomp, builder, useropts):
    return[PlasmaClass(halcomp, builder, useropts)]
