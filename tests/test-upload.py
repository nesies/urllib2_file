#!/usr/bin/env python
# $Id$
# upload a file

import sys
sys.path.insert(0, "..")

import urllib2_file 
import urllib2
import urllib
import string
import StringIO
import getopt

def usage(progname):
    print """SYNTAX: %s -u url -f filename [-s stringio_name]
-f filename : upload this filename
-s name     : upload StringIO file 
"""
    sys.exit(1)
	
if __name__ == '__main__':
    v_url = ""
    v_filename = ""
    v_stringio_name = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                    "hf:s:u:")
    except getopt.GetoptError, errmsg:
        print "ERROR getopt:", errmsg
        usage(sys.argv[0])
        
    for name, value in opts:
        if name in ('-h',):
            usage(sys.argv[0])
        elif name in ('-u', ):
            v_url = value
        elif name in ('-f', ):
            v_filename = value
        elif name in ('-s',):
            v_stringio_name = value
        else:
            print "INVALID argument '%s'" % name
            usage(sys.argv[0])

    if not v_url:
        print "need url= ..."
        usage(sys.argv[0])

    if v_filename == "": 
        print "ERROR: need args --filename=||-s"
        usage(sys.argv[0])
        sys.exit(1)

    fd_file = open(v_filename)
    if v_stringio_name != "":
        # upload a memory file
        print "url=%s upload StringIO memory file" % v_url
        fd = StringIO.StringIO()
        fd.name = v_stringio_name
        fd.write(fd_file.read())
    else:
        print "url=%s upload filename=%s" % (v_url, v_filename)
        fd =  fd_file
	
    post_data = {'file': fd }
    try:
        u = urllib2.urlopen(v_url, post_data)
    except urllib2.HTTPError, error:
        print "ERROR: code=%s message=%s" % (error.code, error.msg)
        sys.exit(1)

    print "HTTP_CODE=%s" % u.code
    print "===begin data_read==="
    print u.read()
    print "===end data_read==="
