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

def gallery_query(url, post_data):
	print "G2 query:", post_data
	u = urllib2.urlopen(url, post_data)
	line = u.readline()
	if line[:-1] != "#__GR2PROTO__":
		print "ERROR: __GR2PROTO__ not found"
		return {"status": "999", "status_text":  "protocol error"}

	res = {}
	line = u.readline() 
	while line != "":
		(key, value) = line[:-1].split("=")
		line = u.readline() 
		res[key] = value
	print "G2 response:", res
	return res

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
	print "# login ..."
	post_data = [	('g2_form[protocol_version]', '2.10'),
			('g2_form[cmd]', 'login'),
			('g2_form[uname]', LOGIN),
			('g2_form[password]', PASSWD),
			('g2_controller', 'remote:GalleryRemote'),
			]
	res_data = gallery_query(URL, post_data)

	if res_data['status'] != '0':
		print "GALLERY ERROR:", res_data
		sys.exit(1)

	auth_token = res_data['auth_token']

	post_data = [	('g2_form[protocol_version]', '2.10'),
			('g2_controller', 'remote:GalleryRemote'),
			('g2_authToken', auth_token),
			('g2_form[cmd]', 'add-item'),
			('g2_form[set_albumName]', ALBUM),
			('g2_userfile', open(FILE)),
		 ]
	print post_data
	headers = {}
#	URL = URL + '?g2_authToken='+auth_token
	req = urllib2.Request(URL, post_data, headers)
	u = urllib2.urlopen(req)
	if not gallery_print_res(u.read()):
		print "GALLERY ERROR"
		sys.exit(1)



