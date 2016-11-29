#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


import traceback
import sys


_SELFS = {}

def breakon(cond):
    global _SELFS
    f = traceback.extract_stack()
    rec = f[-2]
    fname  = rec[0]
    lineno = rec[1]
    assert fname.endswith('.py')
    k = (fname,lineno)
    self = _SELFS.setdefault(k, Obj())
    self.setdefault('breakpoint_active',False)
    if cond:
        if 'next_lineno' not in self:
            next_lineno = get_first_line_of_code(fname,lineno+1)
            self.next_lineno = next_lineno
            assert next_lineno is not None
        sys.settrace.im_self.SetBreak(
            fname,
            self.next_lineno
        )
        self.breakpoint_active = True
    else:
        if self.breakpoint_active:
            sys.settrace.im_self.ClearBreak(
                fname,
                self.next_lineno
            )

__MIC_breakonit_n = None
def breakonit(n):
    """
    break on iteration
    """
    global __MIC_breakonit_n
    if __MIC_breakonit_n is None:
        __MIC_breakonit_n = n
    __MIC_breakonit_n -= 1
    if __MIC_breakonit_n == 0:
        __MIC_breakonit_n = float('inf')
        breakpoint(nback=1, temporary=False)

    a = 3


__MIC_breakonit_n = None
def strbreak(o,s):
    """
    check if str(o) starts with s,
    then break
    """
    v = str(o).startswith(s)
    if v:
        breakpoint(nback=1, temporary=False)

    a = 3





def breakpoint(nback=0,temporary=False):
    from common import wingdb_is_active
    if not wingdb_is_active():
        return
    global _SELFS
    f = traceback.extract_stack()
    rec = f[-nback-2]
    fname  = rec[0]
    lineno = rec[1]
    assert fname.endswith('.py')
    k = (fname,lineno)

    next_lineno = get_first_line_of_code(fname,lineno+1)
    assert next_lineno is not None

    if False:
        sys.settrace.im_self.SetBreak( # python2
            filename = fname,
            lineno = next_lineno,
            temporary = temporary
        )
    else:
        print("SETBREAK: ",
            fname,
            next_lineno,
        )


        sys.settrace.__self__.SetBreak( # python3
            filename = fname,
            lineno = next_lineno,
            temporary = temporary
        )


def get_callers_stackframe():
    global _SELFS
    f = traceback.extract_stack()
    rec = f[-3]
    fname  = rec[0]
    lineno = rec[1]
    from .common import Obj
    o = Obj()
    o.rec = rec
    o.fname  = fname
    o.lineno = lineno
    return o





def get_first_line_of_code(fname,first_line_no):
    """
    line numbers start with 1 (not 0)
    """
    lines = open(fname).readlines()
    for i,l in enumerate( lines[first_line_no-1:] ):
        l = l.strip()
        if len(l):
            if not l.startswith('#'):
                n = first_line_no + i
                return n

    return None


from debtools.common import Obj




