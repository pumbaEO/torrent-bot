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
import gobject
from xdg.BaseDirectory import xdg_config_home, xdg_data_home
#from xdg_support import get_xdg_config_file
from ConfigParser import RawConfigParser as ConfigParser
import logging
#logging.c
CONFIG_FOLDER = join(xdg_config_home, "gomodoro")
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
            self.logdebug("Section \"%s\" not exist, create...", section)
            self._config.add_section(section)
        self._config.set(section,option,value)
        #Dispatcher.config_change(section,option,value)
        self.emit("config-changed",section,option,value)
        
    def write(self):
        filename = get_xdg_config_file("config")
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
            "start_trayicon": "false",
            "fermer_trayicon": "false",
            "use_trayicon": "true",
            "update_title": "true",
            "media_organizer_item" : "0",
            "repeat_mode":"false",
            "shuffle_mode":"false",
            "wikipedia":"en",
            "empty_random":"false",
            "web_font":"Sans 12",
            "web_color_text":"#000000",
            "web_color_link":"#C09665",
            "web_color_bg":"#FFFFFF",
            "web_font":"Sans 12",
            "notification" : "true",
            "compact_playlist" : "false",
            "dynamic_playlist_color": "false",
            "offline" : "false",
            "use_local_cover" : "false" 
            },
            "dynamic_mode":{
            "expanded":"false",
            "enable":"false",
            "remove_played":"true",
            "track_append":"2",
            "track_upcoming":"10",
            "played_show":"3",
            },
            "library":
            {         
#            "location":"",
            "watcher":"false",
            "startup_deleted":"false",
            "startup_added":"false",
            },
            "osd":
            {
                "enable": "false",
                "osd_custom_position": "-1 -1",
                "osd_colors": "#ffffff #ffffff #ffffff #2959ac",
                "osd_font": "Sans 18",
                "osd_timeout": "7.5",
                "osd_transparency": "215",
                "osd_center_x": "1",
                "osd_center_y": "0",
            },
            "audioscrobbler":
            {
                "enable":"false",
                "url":"post.audioscrobbler.com",
                "username":"",
                "password":""
            },
            "lyrics":
            {
                "server":"lyrc.com.ar"
            },
            "player":
            {
                "volume":"1.0",
                "play_on_startup":"false",
                "play":"false",
                "crossfade":"true",
                "crossfade_gapless_album":"false",
                "crossfade_time":"3.0",
                "enqueue":"false",
                "click_enqueue":"false",
                "queuewholealbum":"false",
                "dynamic":"true",
                "vis":"goom",
                "stop_track":"-1",
                "uri":"",
                "state":"stop",
                "seek":"0",
                "selected_track":"-1"
            },
            "window":
            {
            "width" : "860",
            "height" : "530",
            "x" : "-1",
            "y" : "-1",
            "state" : "widthdrawn",
            "pos_organizer" : "130",
            "pos_global_pane" : "270",
            "pos_cur_playlist" : "500",
            "view":"2",
            "right_layout":"false"
            },
            "source":
            {
                "selected_index":"('0','1')",
            },
            "filebrowser":{      
                "pane_pos":"200",
                "uri":"file:///home"
                },
            "browser":
            {
            "view":"0",
            "local_num_cols":"3",

            "podcast_local_num_cols" : "1",

            "jamendo_num_cols":"3",

            "jamendo" : "true",
            "jamendo_last_search":"",
            "jamendo_pos":"120",
            "jamendo_sort_tag":"",
            "jamendo_sort_order":"",

            "local" : "true",
            "local_last_search":"",
            "local_pos":"120",
            "local_sort_tag":"",
            "local_sort_order":"",

            "podcast_local" : "true",
            "podcast_local_last_search":"",
            "podcast_local_pos":"120",
            "podcast_local_sort_tag":"",
            "podcast_local_sort_order":"",

            "daap" : "true",
            "daap_last_search":"",
            "daap_pos":"120",
            "daap_sort_tag":"",
            "daap_sort_order":"",
            "ipod" : "true",
            "ipod_last_search":"",
            "ipod_pos":"120",
            "ipod_sort_tag":"",
            "ipod_sort_order":"",
            "podcast_ipod" : "true",
            "podcast_ipod_last_search":"",
            "podcast_ipod_pos":"120",
            "podcast_ipod_sort_tag":"",
            "podcast_ipod_sort_order":"",
            "filesystem_sort_tag":"",
            "filesystem_sort_order":"",
            "radio_sort_tag":"",
            "radio_sort_order":"",
            "lastfmradio_sort_tag":"",
            "lastfmradio_sort_order":"",
            "favoriteradio_sort_tag":"",
            "favoriteradio_sort_order":"",
            "audiocd_sort_tag":"",
            "audiocd_sort_order":"",
            },
            "song_view": {
                "filesystem_artist":"true",
                "filesystem_artist_order":"1",
                "filesystem_artist_width":"100"
            },
            "podcast":
            {
            "startup":"true",
            "time_refresh":"120",
            "folder":"~/Podcasts",
            "nb_download":"5"
            },
            "iradio":
            {
            "shoutcast_pos":"170"
            },
            "webservice":
            {
            "filter":"bo<###>ost<###>cd1<###>cd2<###>cd3<###>cd 1<###>cd 2<###>cd 3<###> - <###>(<###>)"
            },
            "wikipedia":
            {
            "lang":"en;fr;de;es;it;nl;sv;pl;pt",
            "info":"0"
            },
            "song_editor":
            {
            "width":"476",
            "height":"308"
            },
            "id3": {
                "num0_frame2":"",
                "num0_frame":"TALB",
                "num0_label":_("Album"),
                "num0_tag":"album",
                "num1_frame2":"",
                "num1_frame":"TCOM",
                "num1_label":_("Composer"),
                "num1_tag":"composer",
                "num2_frame2":"",
                "num2_frame":"TCON",
                "num2_label":_("Genre"),
                "num2_tag":"genre",
                "num3_frame2":"",
                "num3_frame":"TDRC",
                "num3_label":_("Year"),
                "num3_tag":"date",
                "num4_frame2":"",
                "num4_frame":"TEXT",
                "num4_label":_("Lyricist"),
                "num4_tag":"lyricist",
                "num5_frame2":"",
                "num5_frame":"TIT2",
                "num5_label":_("Title"),
                "num5_tag":"title",
                "num6_frame2":"",
                "num6_frame":"TIT3",
                "num6_label":_("Version"),
                "num6_tag":"version",
                "num7_frame2":"",
                "num7_frame":"TPE1",
                "num7_label":_("Artist"),
                "num7_tag":"artist",
                "num8_frame2":"TPE1",
                "num8_frame":"TXXX:ALBUM ARTIST",
                "num8_label":_("Album Artist"),
                "num8_tag":"album artist",
                "num9_frame2":"",
                "num9_frame":"TRCK",
                "num9_label":_("#"),
                "num9_tag":"#track"
            },
            "font": {
                "browser_size":"10",
                "library_size":"8"
            },
            "plugins": {
                "active_genericmanager":"Brasero",
                "active_webradiomanager":"Shoutcast",
                "active_sourcemanager":"\n".join(["yooook","Last.fm events","Lastfm Information","Context","Filesystem Browser","Web Radio support"]),
                    }

        }

config = Config()
