#!/usr/bin/env python
# $Id: test.py,v 1.1.1.1 2004-06-24 09:30:02 dakol Exp $
# example upload image to Gallery
# http://gallery.menalto.com/

import urllib2_file 
import urllib2
import urllib
import string
import sys
import getopt
# http//site.com/gallery/gallery_remote2.php
URL=''
LOGIN=''
PASSWD=''
ALBUM=''
FILE=''

def usage(progname):
	print "SYNTAX: %s -U url -L login -P passwd -n album -f file\n\
URL must be http://site.com/gallery/gallery_remote2.php\n\
"
	sys.exit(1)

def gallery_print_res(buffer):
	START='#__GR2PROTO__\n'
	index = string.find(buffer, START)
	if index == -1:
		print "ERROR gallery"
		print buffer
		return False
	print buffer[index+len(START):]
	return True
	
if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:],
								   "hU:L:P:n:f:")
	except getopt.GetoptError, errmsg:
		print "ERROR getopt:", errmsg
		usage(sys.argv[0])

	for name, value in opts:
		if name in ('-h',):
			usage(sys.argv[0])
		elif name in ('-U', ):
			URL = value
		elif name in ('-L', ):
			LOGIN = value
		elif name in ('-P', ):
			PASSWD = value
		elif name in ('-n', ):
			ALBUM = value
		elif name in ('-f', ):
			FILE = value
		else:
			print "INVALID argument '%s'" % name
			usage(sys.argv[0])
			
	if not URL or not LOGIN or not PASSWD or not ALBUM or not FILE:
		print "need args ..."
		usage(sys.argv[0])
	print "URL=%s LOGIN=%s PASSWD=%s ALBUM=%s FILE=%s" % \
		  (URL, LOGIN, PASSWD, ALBUM, FILE)
	
	print "login ..."
	d = [('cmd', 'login'),
		 ('uname', LOGIN),
		 ('password', PASSWD),
		 ('protocol_version', '2.1')
		 ]
	u = urllib2.urlopen(URL, d)
	if not gallery_print_res(u.read()):
		print "GALLERY ERROR"
		sys.exit(1)
	info = u.info()
	cookie=''
	if info.has_key('set-cookie'):
		cookie = info['set-cookie'].split(';')[0]
		print "OK, cookie=", cookie
	else:
		print "KO: no cookie after login"
		sys.exit(1)
	d = [ ('cmd', 'add-item'),
		  ('protocol_version', '2.1'),
		  ('set_albumName', ALBUM),
		  ('userfile', open(FILE)),
		 ]
	headers = {'Cookie': cookie}
	req = urllib2.Request(URL, d, headers)
	u = urllib2.urlopen(req)
	if not gallery_print_res(u.read()):
		print "GALLERY ERROR"
		sys.exit(1)



