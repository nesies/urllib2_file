#!/usr/bin/env python
# $Id$
# upload a file

import sys
sys.path.insert(0, "..")

import os
import urllib2_file 
import urllib2
import urllib
import string
import StringIO
import cStringIO
import getopt

def usage(progname):
    print """SYNTAX: %s -u url -f filename [-s StringIO_name] [-c cStringIO_name] 
         [-p foo=bar] [-n form_name]
-u url

-f path/to/file          : upload this file
-F filename              : upload with this filename ("file.txt")
-s StringIO_filename     : upload StringIO file 
-c cStringIO_filename    : upload StringIO file 
-n form_name             : change default name in <INPUT TYPE="file" NAME="form_name" />
-p foo=bar               : add a name,value to the request (<INPUT TYPE="text" NAME="foo" VALUE="bar" />)

*) upload filename
    test-upload.py -u url -f filename

*) upload filename with StringIO form_nname=file01 and filename=file01
    test-upload.py -u url -f filename -s file01

*) upload filename with cStringIO form_name=file01 and filename=file01
    test-upload.py -u url -f filename -c file01

*) upload filename with StringIO form_name=file01 and filename=recipe.txt
    test-upload.py -u url -f filename -s file01 -n recipe.txt

*) upload filename with form_name=file01 and filename=filename
    test-upload.py -u url -f filename -n file01

*) upload filename with default form_name and filename=filename01
    test-upload.py -u url -f filename -F filename01

*) upload filename with form_name=form_file01 and filename=filename01
    test-upload.py -u url -f filename -n form_file01 -F filename01

*) upload filename with default form_name and filename=filename AND with form data foo=bar
    test-upload.py -u url -f filename -p foo=bar

"""
    sys.exit(1)
	
if __name__ == '__main__':
    v_post = {}
    v_url = ""
    v_file = ""
    v_filename = ""
    v_form_name = "default_form_name"
    v_stringio_filename = ""
    v_cstringio_filename = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                    "hc:f:F:n:p:s:u:")
    except getopt.GetoptError, errmsg:
        print "ERROR getopt:", errmsg
        usage(sys.argv[0])
        
    for name, value in opts:
        if name in ('-h',):
            usage(sys.argv[0])
        elif name in ('-u', ):
            v_url = value
        elif name in ('-f', ):
            v_file = value
        elif name in ('-F', ):
            v_filename = value
        elif name in ('-n', ):
            v_form_name = value
        elif name in ('-p', ):
            tmp = value.split("=")
            if len(tmp) == 2:
                v_post[tmp[0]] = tmp[1]
            else:
                print "ERROR: -p name:value excepted"
                sys.exit(-1)
        elif name in ('-s',):
            v_stringio_filename = value
        elif name in ('-c',):
            v_cstringio_filename = value
        else:
            print "INVALID argument '%s'" % name
            usage(sys.argv[0])

    if not v_url:
        print "need url= ..."
        usage(sys.argv[0])

    if v_file == "": 
        print "ERROR: need args -f file"
        usage(sys.argv[0])
        sys.exit(1)
    
    fd_file = open(v_file)

    filename = ""
    if v_stringio_filename != "":
        # upload a memory file
        print "url=%s upload StringIO memory file" % v_url
        fd = StringIO.StringIO()
        filename = v_stringio_filename
        fd.write(fd_file.read())
    elif v_cstringio_filename != "":
        # upload a memory file
        print "url=%s upload cStringIO memory file" % v_url
        fd = cStringIO.StringIO()
        filename = v_cstringio_filename
        fd.write(fd_file.read())
    else:
        print "url=%s upload filename=%s" % (v_url, v_filename)
        fd =  fd_file

    # force filename   
    if v_filename != "":
        filename = v_filename
 
    post_data = v_post

    if filename == "":
        post_data[v_form_name] = fd 
    else:
        post_data[v_form_name] = {  'fd':       fd,
                                    'filename': filename}
    print "post_data=", post_data

    try:
        u = urllib2.urlopen(v_url, post_data)
    except urllib2.HTTPError, error:
        print "ERROR: code=%s message=%s" % (error.code, error.msg)
        sys.exit(1)

    print "HTTP_CODE=%s" % u.code
    print "===begin data_read==="
    print u.read()
    print "===end data_read==="

