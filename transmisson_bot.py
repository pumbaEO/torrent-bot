#!/usr/bin/python

from jabberbot import JabberBot, botcmd
import datetime

from simplejson import dumps, loads
from urllib import urlopen
import sys
import httplib
import transmissionrpc

class TransmissionClientFailure(Exception): pass

class TransmissionClientRpc(object):
    user="transmission"
    password = "transmission"
    def __init__(self):
        try:
            self._getSessionID()
        except Exception, e:
            raise TransmissionClientFailure, \
                "Make 1 sure your transmission-daemon is running  %s" % e
    def _getSessionID(self):
        self.client = transmissionrpc.Client('127.0.0.1',user='transmission',password='transmission')
    def sessionStats(self):
        self.session = self.client.session_stats()
        return self.session.fields
    

class TransmissionClient(object):
  
  rpcUrl = None
  sessionId = None
  def __init__( self, rpcUrl='http://localhost:9091/transmission/rpc' ):
    """ try to do a stupid call to transmission via rpc """

    try:
      self.rpcUrl = rpcUrl
      #Nathan Stehr: June 4, 2009: 
      #the new version of transmission uses a session key, so make a dummy
      #request and get the session id from the headers 
      self._getSessionID()

    except Exception, e:
      raise TransmissionClientFailure, \
            "Make sure your transmission-daemon is running  %s" % e


  def _getSessionID(self):
       conn = httplib.HTTPConnection("localhost:9091")
       conn.request("GET", "/transmission/rpc?")
       response = conn.getresponse()
       self.sessionId = response.getheader('x-transmission-session-id')
  
  def _rpc( self, method, params=[] ):
    """ generic rpc call to transmission """

    postdata = dumps({ 'method': method, 
                       'arguments': params, 
                       })
    
    try:
        conn = httplib.HTTPConnection("localhost:9091")
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","x-transmission-session-id":self.sessionId}
        conn.request("POST", "/transmission/rpc", postdata,headers)
        response = conn.getresponse()
        status = response.status
        if status==409:
            self._getSessionID()
            self._rpc(method,params)
        data = response.read()
        conn.close()
        return loads(data)
    except Exception, e:
      raise TransmissionClientFailure, \
            "Make sure your transmission-daemon is running  %s" % e

    return response



  def sessionStats( self ):
    return self._rpc( 'session-stats' )


  def torrentGet( self, torrentIds='', fields=[ 'id', 'name']):
    if torrentIds == '':
        return self._rpc( 'torrent-get', {'fields': fields } )
    else:
        return self._rpc( 'torrent-get', { 'ids': torrentIds, 'fields': fields } ) 

  def torrentAdd( self, torrentFile, downloadDir='.' ):
    return self._rpc( 'torrent-add', { 'filename': torrentFile, 
                                      'download-dir': downloadDir } )


  def torrentRemove( self, torrents=None ):
    return self._rpc( 'torrent-remove', { 'ids': torrents } )


  def sessionSet( self, key, value ):
    return self._rpc( 'session-set', { key: value } )

  
  def sessionGet( self ):
    return self._rpc( 'session-get' )


class SystemInfoJabberBot(JabberBot):
    @botcmd
    def serverinfo( self, mess, args):
        """Displays information about the server"""
        version = open('/proc/version').read().strip()
        loadavg = open('/proc/loadavg').read().strip()

        return '%s\n\n%s' % ( version, loadavg, )
    
    @botcmd
    def time( self, mess, args):
        """Displays current server time"""
        return str(datetime.datetime.now())

    @botcmd
    def rot13( self, mess, args):
        """Returns passed arguments rot13'ed"""
        return args.encode('rot13')

    @botcmd
    def whoami( self, mess, args):
        """Tells you your username"""
        return mess.getFrom()

    @botcmd
    def overview(self, mess, args):
        """Overview of torrent client current state"""
        client = TransmissionClientRpc()
        results = client.sessionStats()
        #arguments = results['arguments']
        uploadSpeed = results['uploadSpeed']
        uploadSpeed = float(uploadSpeed)/1000
        uploadSpeed = str(uploadSpeed) + " kb/s"
        downloadSpeed = results['downloadSpeed']
        downloadSpeed = float(downloadSpeed)/1000
        downloadSpeed = str(downloadSpeed) + " kb/s"
        activeTorrents = str(results['activeTorrentCount'])
        pausedTorrents = str(results['pausedTorrentCount'])
        totalTorrents = str(results['torrentCount'])
        output = "Download Speed: "+downloadSpeed+"\n"
        output = output + "Upload Speed: "+uploadSpeed+"\n"
        output = output + "Number of Active Torrents: " + activeTorrents+"\n"
        output = output + "Number of Paused Torrents: " + pausedTorrents+"\n"
        output = output + "Total Number of Torrents: " + totalTorrents
        return output

    @botcmd
    def alltorents(self, mess, args):
        client = TransmissionClient()
        torrents = self.getTorrentList(client)
        if len(torrents) == 0:
            output = "No torrents in the system"
        for torrent in torrents:
            output = output+self.calculateTorrentMsg(torrent)
        return output

    def calculateTorrentMsg(self,torrent):
        name = torrent['name']
        totalSize = float(torrent['totalSize'])/1048576
        totalSize = round(totalSize,3)
        #downloaded = float(torrent['downloadedEver'])/1048576
        #downloaded = round(downloaded,3)
        #going to calculate current downloaded amount based on the files array.  The above method seems to be off when
        #the client has been stopped and restarted
        files = torrent['files']
        
        sum = 0
        for file in files:
            sum = sum+file['bytesCompleted']
        downloaded = float(sum) / 1048576
        downloaded = round(downloaded,3)
        downloadRate = float(torrent['rateDownload'])/1000
        downloadRate = round(downloadRate,3)
        uploadRate = float(torrent['rateUpload'])/1000
        uploadRate = round(uploadRate,3)
        percent = (downloaded/totalSize)*100
        percent = round(percent,3)
              

        torrentMsg = "Name: "+name+"\n"
        torrentMsg = torrentMsg + "Total Size: "+str(totalSize)+" MB \n"
        torrentMsg = torrentMsg + "Downloaded So Far: "+str(downloaded) +" MB \n"
        torrentMsg = torrentMsg + "Percent Completed: "+ str(percent)+" %\n"
        torrentMsg = torrentMsg + "Download Rate: " + str(downloadRate) + " kb/s \n"
        torrentMsg = torrentMsg + "Upload Rate: " + str(uploadRate) + " kb/s \n"
             

        remaining = totalSize-downloaded
        remaining = remaining * 1024 
        if remaining > 0:
            if downloadRate > 0:
                #time in seconds
                time = remaining/downloadRate
                time = uptime(time)
                torrentMsg = torrentMsg +"Time Remaining "+ time +"\n"
            else:
                torrentMsg = torrentMsg +"Time Remaining ? \n"
        else:
            torrentMsg = torrentMsg +"Download complete \n"
        output = torrentMsg+"-----\n"
        return output


 
username = 'smsshenjasosna@gmail.com'
password = 'nokiaXpressMusic'
bot = SystemInfoJabberBot(username,password)
bot.serve_forever()
