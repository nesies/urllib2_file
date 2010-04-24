#!/usr/bin/env python
# $Id$
import os
import random
import socket
import string
import sys
import tempfile
import time
import unittest
import urllib2
import urllib

import testHTTPServer

tmp = os.path.join(os.path.dirname(sys.argv[0]), '..')
sys.path.insert(0, tmp)
import urllib2_file

class TestSequenceFunctions(unittest.TestCase):
    url = 'http://127.0.0.1:32800/upload'

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        fd = open(self.tempdir + os.sep + "filename_01.txt", "w")
        fd.write("filename_01 data of file one")
        fd.close()

        fd = open(self.tempdir + os.sep + "filename_02.txt", "w")
        fd.write("filename_02 data of file two")
        fd.close()

    def tearDown(self):
        pass

    def job(self, method, data, response_expected_list, willSucceed=True):
        if method == 'GET':
            url = self.url + '?' + urllib.urlencode(data)
            u = urllib2.urlopen(url)
        elif method == 'POST':
            u = urllib2.urlopen(self.url, data)

        response_got = u.read()
        errors = 0
        for response in response_expected_list:
            if -1 == string.find(response_got, response):
                if willSucceed:
                    self.fail(response + " not found in " + response_got)
                errors += 1
        if not willSucceed and errors == 0:
            self.fail("did not failed as expected")

    def test_form_void(self):
        self.job('POST', "pouet", 'NO_FORM_DATA')

    def test_form_name1(self):
        data = {"foo": "bar"}
        response_expected = [ ( 'POST_VAR name=foo value=bar <br/>\n' ) ]
        self.job('POST', data, response_expected)

    def test_form_name1_fail(self):
        data = {"foo": "bar"}
        response_expected = [ ( 'FAIL name=foo value=bar <br/>\n' ) ]
        self.job('POST', data, response_expected, False)
   
    def test_form_name1_get(self):
        data = {"foo": "bar"}
        response_expected = [ ( 'GET_VAR name=foo value=bar <br/>\n' ) ]
        self.job('GET', data, response_expected)
        
    def test_form_name1_name2(self):
        data = {"name1":    "value1",
                "name2":    "value2" }
        
        response_expected = []
        response_expected.append('POST_VAR name=name1 value=value1 <br/>\n')
        response_expected.append('POST_VAR name=name2 value=value2 <br/>\n')

        self.job('POST', data, response_expected)

    def test_form_file1(self):
        fd1 = open(self.tempdir + os.sep + "filename_01.txt")
        length1 = len(fd1.read())
        fd1.seek(0)

        data = {"file01": fd1}
        response_expected = [ ( 'POST_FILE name=file01 filename=file01 length=%d <br/>\n' % length1 ) ]
        self.job('POST', data, response_expected)

    def test_form_file1_name(self):
        fd1 = open(self.tempdir + os.sep + "filename_01.txt")
        length1 = len(fd1.read())
        fd1.seek(0)

        data = {'file01': { 'fd': fd1,
                            'filename': 'filename01'}}
            
        response_expected = [ ( 'POST_FILE name=file01 filename=filename01 length=%d <br/>\n' % length1 ) ]
        self.job('POST', data, response_expected)

    def test_form_name1_file1(self):
        fd1 = open(self.tempdir + os.sep + "filename_01.txt")
        length1 = len(fd1.read())
        fd1.seek(0)

        data = { "foo":  "bar",
                "file01": fd1}

        response_expected = []
        response_expected.append( 'POST_VAR name=foo value=bar <br/>\n' )
        response_expected.append( 'POST_FILE name=file01 filename=file01 length=%d <br/>\n' % length1 )

        self.job('POST', data, response_expected)

    def test_form_file1_file2(self):
        fd1 = open(self.tempdir + os.sep + "filename_01.txt")
        length1 = len(fd1.read())
        fd1.seek(0)

        fd2 = open(self.tempdir + os.sep + "filename_02.txt")
        length2 = len(fd2.read())
        fd2.seek(0)

        data = {"file01": fd1,
                "file02": fd2 }

        response_expected = []
        response_expected.append( 'POST_FILE name=file01 filename=file01 length=%d <br/>\n' % length1 )
        response_expected.append( 'POST_FILE name=file02 filename=file02 length=%d <br/>\n' % length2 )

        self.job('POST', data, response_expected)

        
    def test_form_file1_file2(self):
        fd1 = open(self.tempdir + os.sep + "filename_01.txt")
        length1 = len(fd1.read())
        fd1.seek(0)

        fd2 = open(self.tempdir + os.sep + "filename_02.txt")
        length2 = len(fd2.read())
        fd2.seek(0)

        data = {'file01': { 'fd':       fd1,
                            'filename': 'filename01',},
                'file02': { 'fd':       fd2 ,
                            'filename': 'filename02',}}

        response_expected = []
        response_expected.append( 'POST_FILE name=file01 filename=filename01 length=%d <br/>\n' % length1 )
        response_expected.append( 'POST_FILE name=file02 filename=filename02 length=%d <br/>\n' % length2 )

        self.job('POST', data, response_expected)
def test_suite():
    print sys.argv[0]
    # start http server
    listen_port_start = 32800
    for listen_port in range(listen_port_start, listen_port_start + 10):
        # print "trying to bind on port %s" % listen_port
        httpd = testHTTPServer.testHTTPServer('127.0.0.1', listen_port, )
        try:
            httpd.listen()
            break
        except socket.error, (errno, strerr):
            # already in use
            if errno == 98:
                continue
            else:
                print "ERROR: listen: ", errno, strerr 
                sys.exit(-1)
    print "http server bound to port", listen_port
    httpd.start()
    while not httpd.isReady():
        time.sleep(0.1)
    u = urllib2.urlopen('http://127.0.0.1:32800/ping') 
    data = u.read()
    if data != "pong":
        print "error"
        sys.exit(-1)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    results = unittest.TextTestRunner(verbosity=2).run(suite)

    httpd.die()
    httpd.join()
    print "http server stopped"
    return results

if __name__ == '__main__':
    test_suite()
    
