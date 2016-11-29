#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


print("ASDFASDF")

globs = globals()
import sys

print(sys.argv)
from pprint import pprint

if False:
    fname = sys.argv[-1]
    fname = eval(fname)
else:
    if False:
        fname = sys.argv[1]
        assert sys.argv[0] == "-m"
        del sys.argv[0]
    else:
        fname = sys.argv[1]
        del sys.argv[0]




import contextlib
import os
import os.path as pathmod
import glob


@contextlib.contextmanager
def chdir(dirname=None):
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)




with open(fname) as f:
    print("MIC: STARTING", fname)

    code = compile(f.read(), fname, 'exec')
    #global_vars = dict(globals())
    #global_vars['__name__'] = '__main__'
    #}
    local_vars = {}
    main_globals = sys.modules["__main__"].__dict__
    global_vars = dict(main_globals)
    if True:
        #mod_name = "__main__"
        patch = dict(
            __name__ = "__main__",
            __file__ = fname,
            __cached__ = None,
            #__doc__ = "blabla",
            #__loader__ = loader,
            __package__ = None,
            #__spec__ = mod_spec
        )
        global_vars.update(patch)
    #exec(code, global_vars, local_vars)
    #global_vars["_mic"] = print
    #pprint(global_vars)
    sys.stdout.flush()
    if False:
        import time
        time.sleep(1)
    #__builtins__["search"] = 32
    import os
    dirpath = pathmod.abspath(pathmod.join(
        pathmod.dirname(__file__),
        ".."
    ))
    #print("dirpath:",__file__)
    #dirpath = "."
    sys.path.insert(0, dirpath)
    from debtools.hotswap import roc
    from debtools.finding import findobjectpath
    from debtools.tracing import trac, gettrac
    from debtools.breaking import breakpoint
    #from common import Obj, G, p
    #from debtools.common import *
    from debtools import common
    from debtools import hotswap
    from debtools import finding
    from debtools import tracing
    from debtools import breaking
    del sys.path[0]
    __builtins__.__dict__["roc"] = hotswap.roc
    __builtins__.__dict__["findobjectpath"] = finding.findobjectpath
    __builtins__.__dict__["trac"] = tracing.trac
    __builtins__.__dict__["breakpoint"] = breaking.breakpoint
    __builtins__.__dict__["reload"] = hotswap.reload_any
    #o = Obj()
    G = common.G
    __builtins__.__dict__["dd"] = common.G
    __builtins__.__dict__["p"] = common.p
    G.settrace = sys.settrace
    G.gettrac = gettrac
    G.common = common
    G.hotswap = hotswap
    #trac()
    exec(code, global_vars, None) #{"aaa": 234})

