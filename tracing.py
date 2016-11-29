#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import sys

#sys.path.insert(0, dirpath)
#from hotswap import roc
#from finding import findobjectpath
#from tracing import trac
print("NNNAAAA", __name__)
from debtools.breaking import breakpoint
#del sys.path[0]
import pickle

#from .breaking import breakpoint
from debtools.common import G

old_count = 0
FNAME = "/tmp/mic_tracdata.pkl"

def gettrac():
    o = pickle.load(open(FNAME,"rb"))
    return o

def trac():
    G.tracdata = []

    def trace_calls(frame, event, arg):
        if event != 'call':
            return
        co = frame.f_code
        func_name = co.co_name
        if func_name == 'write':
            return
        func_line_no = frame.f_lineno
        func_filename = co.co_filename
        caller = frame.f_back
        caller_line_no = caller.f_lineno
        caller_filename = caller.f_code.co_filename
        dat = G.tracdata
        dat.append((
            func_line_no,
            func_filename,
            #caller,
            caller_line_no,
            caller_filename,
        ))
        n = len(dat)
        global old_count
        if  n > old_count + 2000:
            print("dumping")
            f = open(FNAME, "wb")
            pickle.dump(dat, f)
            old_count = n

        #if "offline" in func_name or True:
        if "offline" in func_name:
            #print()
            #sys.settrace.__self__.Stop()
            #raise RuntimeError("blabla")
            #import pdb; pdb.set_trace()
            #sys.settrace(print)
            #breakpoint(nback=2)
            #print("CALL", func_name)

            print("***** FOUND FUNC CALL")
            print("func name      %s()"%func_name)
            print("func lineno   ", func_line_no)
            print("file          ", func_filename)
            print("caller        ", caller_filename)
            print("caller lineno ", caller_line_no)

            if False:
                input("press enter")
                #import time
                #time.sleep(10)
        else:
            return

        print(
            'Call to %s on line %s of %s from line %s of %s' % (
                func_name,
                func_line_no,
                func_filename,
                caller_line_no,
                caller_filename
            )
        )
        return

    #if False:
    if True:
        dd.settrace(trace_calls)
    else:
        sys.settrace(trace_calls)
    #try:
        #sys.settrace(trace_calls)
    #except RuntimeError as e:
        #print(e)
