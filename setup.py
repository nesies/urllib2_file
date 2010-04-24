from distutils.core import setup
from distutils.core import Command
import glob
import os
import os.path
import sys
import unittest

class TestCommand(Command):
    user_options = [ ]
        
    def initialize_options(self):
        self.test_dirs = None
 
    def finalize_options(self):
        if self.test_dirs is None:
            self.test_dirs = ['tests', ]
    
    def run(self):
        errors =  0
        failures = 0
        for dir in self.test_dirs:
            for filename in glob.glob(os.path.join(dir, "test_*.py")):
                self.announce("running test from " + filename)
                info = self._run_test(filename)
                errors = errors + info[0]
                failures = failures + info[1]
        if errors or failures:
            self.announce("%d errors and %d failures" % (errors, failures)) 

    def _run_test(self, filename):
        dirname, basename = os.path.split(filename)
        sys.path.insert(0, dirname)
        try:
            modname = os.path.splitext(basename)[0]
            mod = __import__(modname)
            if hasattr(mod, "test_suite"):
                results = mod.test_suite()
                return len(results.errors), len(results.failures)
            else:
                return (0, 0)
        finally:
            if sys.path[0] == dirname:
                del sys.path[0]

setup(name="urllib2_file",
	version='0.2.1',
	description='urllib2 extension which permit HTTP POST upload',
	author='Fabien SEISEN',
	author_email='fab@seisen.org',
	url='http://fabien.seisen.org/python/',
	py_modules=['urllib2_file'],
    cmdclass = {'test': TestCommand }
	)

