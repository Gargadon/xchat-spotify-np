"""
    Spotify Now Playing Script
    Requires Python, Xchat, Spotify and DBus

    Erik Nosar
    Modified by David Kantun
    Script released under Public Domain
"""

__module_name__         = "xchat-spotify-np"
__module_version__      = "2.2"
__module_description__  = "Now playing script for Spotify for XChat on Linux"

import xchat
import os
import re
import dbus

"""
Sample data contained from within the following dbus call:
    trackinfo = spotify.Get("org.mpris.MediaPlayer2.Player","Metadata")

dbus.Dictionary(
    {dbus.String(u'xesam:album'): dbus.String(u'A State Of Trance Episode 631', variant_level=1),
    dbus.String(u'xesam:title'): dbus.String(u'Daylight [ASOT 631] - Philippe El Sisi Remix', variant_level=1),
    dbus.String(u'xesam:trackNumber'): dbus.Int32(27, variant_level=1),
    dbus.String(u'xesam:artist'): dbus.Array([dbus.String(u'Jumpy Jumps')], signature=dbus.Signature('s'), variant_level=1),
    dbus.String(u'xesam:discNumber'): dbus.Int32(0, variant_level=1),
    dbus.String(u'mpris:trackid'): dbus.String(u'spotify:track:59PulgxMdbrXRA4ScxuHaJ', variant_level=1),
    dbus.String(u'mpris:length'): dbus.UInt64(251000000L, variant_level=1),
    dbus.String(u'mpris:artUrl'): dbus.String(u'http://open.spotify.com/thumb/98ce7987aa9944788ffdc50b8605a38f1e66de16', variant_level=1),
    dbus.String(u'xesam:autoRating'): dbus.Double(0.45, variant_level=1),
    dbus.String(u'xesam:contentCreated'): dbus.String(u'2013-01-01T00:00:00', variant_level=1),
    dbus.String(u'xesam:url'): dbus.String(u'spotify:track:59PulgxMdbrXRA4ScxuHaJ', variant_level=1)},
    signature=dbus.Signature('sv'), variant_level=1)

"""

def on_nowplaying(word, word_eol, userdata):
    bus = dbus.SessionBus()
    if bus.name_has_owner('org.mpris.MediaPlayer2.spotify'):
	   spotify = bus.get_object('org.mpris.MediaPlayer2.spotify','/org/mpris/MediaPlayer2')
           # Get current channel and get latest track from Spotify
           context = xchat.get_context()
           channel = context.get_info("channel")
	   metadatas = dbus.Interface(spotify,'org.freedesktop.DBus.Properties')
	   trackinfo = metadatas.Get('org.mpris.MediaPlayer2.Player','Metadata')
           # Get track information from DBus dictionary
           album       = unicode(trackinfo.get("xesam:album")).encode('utf-8')
           title       = unicode(trackinfo.get("xesam:title")).encode('utf-8')	
           trackNumber = str(unicode(trackinfo.get("xesam:trackNumber")).encode('utf-8'))
	   discNumber  = str(unicode(trackinfo.get("xesam:discNumber")).encode('utf-8'))
	   trackid     = str(unicode(trackinfo.get("xesam:trackid")).encode('utf-8'))
	   length      = unicode(trackinfo.get("xesam:length")).encode('utf-8')
	   artUrl      = unicode(trackinfo.get("xesam:artUrl")).encode('utf-8')
	   url         = unicode(trackinfo.get("xesam:url")).encode('utf-8')
    # The artist list is provided as an array. Combine all artists to a single string.
	   artist = str(unicode(", ".join(trackinfo.get("xesam:artist"))).encode('utf-8')).strip()
	   npmsg = "Now playing on 02Spotify: %s - %s [%s] (%s)" % (artist, title, album, url)
	   xchat.command("msg %s %s" % (channel, npmsg))
	   return xchat.EAT_ALL
    else:
	   return xchat.EAT_ALL    
    
xchat.hook_command("spotify", on_nowplaying)
xchat.prnt("/spotify - Announce currently playing track in Spotify")