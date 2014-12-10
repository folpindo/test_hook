#/bin/evn python

import sys
import os

from subprocess import Popen, PIPE, call

class ProcessContainer(object):

    hooks = []

    def __init__(self):
        pass

    def add(self,hook):
        self.hooks.append(hook)

    def get_hooks(self):
        return self.hooks

    def print_ret(self,ret):
	print "cli_output: %s" % ret['cli_output']
	print "exit_code: %s" % ret['exit_code']

    def run(self):
        hooks = self.hooks
        for h in hooks:    
            if h.get_type() is 'bash':
                ret = h.run_sh()
		self.print_ret(ret)
            elif h.get_type() is 'python':
                ret = h.run_python()
		self.print_ret(ret)
            else:
                print "Type not recognized."
                        
class Hook(object):

    script = None
    script_type = None
    
    def __init__(self,script,script_type):
        self.script = script
        self.script_type = script_type
        
    def initialized(self):
        return (self.script is not None)

    def __run(self,prog):
        prun = Popen([prog, self.script], stdout=PIPE)
        res = prun.communicate()[0]
        prun.stdout.close()
        return {'cli_output':res,'exit_code':prun.returncode}

    def run_sh(self):
        if self.initialized():
            return self.__run('/bin/sh')
    
    def run_python(self):
        if self.initialized():
            return self.__run('/usr/bin/python')
        
    def set_script(self,script):
        self.script = script
        
    def set_type(self,script_type):
        self.script_type = script_type
        
    def get_type(self):
        return self.script_type
