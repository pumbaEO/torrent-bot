#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'Sosna'
__version__ = '0.0.1'
import urllib
import urllib2
import cookielib
import optparse
import re
import xmllib
import logging
import gettext
from gettext import gettext as _
gettext.textdomain('diffsamizdat')
logging.getLogger()

post_params = urllib.urlencode({
    'login_username' : LOGIN,
    'login_password' : PASS,
    'login' : '%C2%F5%EE%E4'
})


class BaseHtmlParser(sgmllib.SGMLParser):

    def reset(self):
        self.ddflag = 0
        self.data = ""
        sgmllib.SGMLParser.reset(self)
    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.data = []
        self.hyperlinks = []
    def parse(self, s):
        self.feed(s)
        self.close()

    def start_a(self, attr):
        "Process a hyperlink and its 'attributes '."
        is_id = False
        for name, value in attr:
            if name == "href":
                if value == 'http://google.com':
                    is_id = True
                self.hyperlinks.append(value)
            elif name == "onclick" and is_id:
                self.data.append(value)
    def get_hyperlinks(self):
        return self.hyperlinks
    def get_data(self):
        return self.data


class TorrentCheck:
    def __init__(self):
        LOGIN   = 'login'
        PASS    = 'pass'
        self.post_params = urllib.urlencode({
                                'login_username' : LOGIN,
                                'login_password' : PASS,
                                'login' : '%C2%F5%EE%E4'
                                        })
        self._connect()
        self.check_url('107803')
    def _connect(self):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)
        # авторизация + сессия с куками
        self.web_obj = self.opener.open('http://pirat.ca/forum/login/', self.post_params)
        logging.debug(_("login in site"))
        #web_obj = opener.open('http://login.rutracker.org/forum/login.php', post_params)
        self.data = self.web_obj.read()

    def dw_torrent_f(self, b_data, f_name):
        f = open(f_name+'.torrent','w')
        f.write(b_data)
        f.close()
    def check_url(self, id):
        topic_url = 'http://pirat.ca/topic/'+id
        self.web_obj= self.opener.open(topic_url, self.post_params)
        data = self.web_obj.read()
        d = re.findall()
        parser = BaseHtmlParser()
        parser.parse(data)
        print parser.get_data()
    def parsexml(self, data):

        from xml.etree.ElementTree import parse
        import xml.etree.ElementTree
        from xml.dom.minidom import parse as parsemini
        import xml.dom.minidom

        Dom = parsemini(data)
        etreepatch = parse(data)
        
LEVELS = (  logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
            )
def main():
	usage = _("torrent_download [options]")
	parser = optparse.OptionParser(version="diffsamizdat %s" % __version__, usage=usage)
	parser.add_option('-d', '--debug', dest='debug_mode', action='store_true',
	help=_('Print the maximum debugging info (implies -vv)'))
	parser.add_option('-v', '--verbose', dest='logging_level', action='count',
		help=_('set error_level output to warning, info, and then debug'))
	
	parser.set_defaults(logging_level=0)
	(options, args) = parser.parse_args()
	# set the verbosity
	if options.debug_mode:
		options.logging_level = 3
	logging.basicConfig(level=LEVELS[options.logging_level], format='%(lineno)d %(asctime)s %(levelname)s %(message)s')
	t = TorrentCheck()
	return 

if __name__=='__main__':
	main()
