# -*- coding: utf-8 -*-

# Copyright (C) 2011 Shenja Sosna <shenja at sosna.zp.ua>

# This file is part of Torrents check bot.

# Project Hamster is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Project Hamster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Project Hamster.  If not, see <http://www.gnu.org/licenses/>.

"""
this code copied from Mehdi Abaakouk <theli48@gmail.com> via Listen, 2006 Mehdi AbaakoukGimmie (c) 
License: GPLv2
"""
from xdg.BaseDirectory import xdg_config_home, xdg_data_home
#from xdg_support import get_xdg_config_file
from ConfigParser import RawConfigParser as ConfigParser
import logging
logging.getLogger("TorrentCheck")

CONFIG_FOLDER = join(xdg_config_home, "torrentcheck")
VERSION_CONFIG=1

class Config():
    
    def __init__(self):
        self._config = ConfigParser()
        self.getboolean = self._config.getboolean
        self.getint = self._config.getint
        self.getfloat = self._config.getfloat
        self.options = self._config.options
        self.has_option = self._config.has_option
        self.remove_option = self._config.remove_option
        self.add_section = self._config.add_section

        for section, values in self.__get_default().iteritems():
            self._config.add_section(section)
            for key, value in values.iteritems():
                self._config.set(section, key, value)
    

    def load(self):
		self._config.read( CONFIG_FOLDER )
		self.update_config()

    def update_config(self):
        version = self.get("setting","version", "")
        if not version:
			logging.debug("not version")
            #self.set("wikipedia","lang", self.get("wikipedia","lang").replace("<###>",";"))
        self.set("setting","version",VERSION_CONFIG)
        self.write()
        
    def get(self,section,option,default=None):
        if default is None:
            return self._config.get(section,option)
        else:
            try: 
                return self._config.get(section,option)
            except: 
                return default

    def set(self,section,option,value):
        if not self._config.has_section(section):
            logging.debug("Section \"%s\" not exist, create...", section)
            self._config.add_section(section)
        self._config.set(section,option,value)
        #Dispatcher.config_change(section,option,value)
        
    def write(self):
        filename = CONFIG_FOLDER
        f = file(filename, "w")
        self._config.write(f)
        f.close()

    def state(self, arg):
        return self._config.getboolean("setting", arg)

    def __get_default(self):
        return {
            "plugins":{
                    },
            "setting":
            {
            "username": "pumbaEO",
            "password": "password",
            }

        }

config = Config()
