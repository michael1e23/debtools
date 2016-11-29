#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os

class Obj(object):
    pass


def wingdb_is_active():
    v = 'WINGDB_ACTIVE' in os.environ
    return v


G = Obj()

from pprint import pprint,pformat

import types
def formatfunc(func):
    lno = func.__code__.co_firstlineno
    fname = func.__code__.co_filename
    lines = open(fname).readlines()
    lines = lines[lno-4:lno+4]
    code = "".join(lines)
    idx = code.find("def")
    if idx != -1:
        code = code[idx:]
    code = code.strip()
    code += "\n..."

    s = ""
    s += "\n"
    s += "    *** function ***\n"
    s += "  file   : {} : {}\n".format(fname, lno)
    s += "  module : {}\n".format(func.__module__)
    s += "\n"
    s += code
    #s = code

    return s


def myprint(*args):
    multiline = False
    l = []
    for a in args:
        if isinstance(a, types.FunctionType):
            s = formatfunc(a)
        else:
            if hasattr(a,"__dict__"):
                dct = a.__dict__
            elif hasattr(a, "_asdict"):
                dct = a._asdict()

            if dct is not None:
                s1 = items_to_str(dct.items())
                #s1 = items_to_str(a.__dict__.items())
                s2 = pformat(a)
                s = s1 + "\n" + s2
            else:
                s = pformat(a)
        if "\n" in s:
            multiline = True
        l.append(s)

    if multiline:
        s = ",\n".join(l)
    else:
        s = ", ".join(l)

    print(s)





class _P:
    def __call__(self, *args):
        myprint(*args)


    def __truediv__(self, o):
        myprint(o)

p = _P()






from collections import OrderedDict

def items_to_str(items, verbosity=0):
    #print("AAA6")
    itemdict = OrderedDict(items)

    delt = 1 - verbosity
    #with print_depth(delt=delt) as dep:
    if True:
        dep = 0
        max_vs_len = 77
        max_ks_len = 20 # _MIC_MAX_KEY_FORMAT_LEN

        if dep > 1:
            s = ','.join(
                map(str,self.keys())
            )
            s = '{%s}'%s
            return s


        #kl = np.max( map(len,self.__dict__.keys()) )
        lens = list(map(lambda x: len(str(x)), itemdict.keys()))
        kl = max(lens)
        #kl = np.max(  )
        #kl = np.max( map(lambda x: len(str(x)),self.__dict__.keys()) )
        l  = []
        d = itemdict
        #d = self.__dict__
        #hids = self._MIC_hidden_attributes
        keys = itemdict.keys()
        for k in keys: #self._MIC_attribute_order:
            #if not d.has_key(k):
                #continue
            #if k in hids:
                #continue
            v = d[k]
            ks = str(k)
            pad = kl - len(ks)
            vs = str(v)
            #if verbosity < 0:
            if dep > -1:
                #vs = vs.replace('\n',' ')
                vs = vs.replace(',\n',', ')
                vs = vs.replace('\n',' \\ ')
                while True:
                    ttt = vs.replace('  ',' ')
                    if len(ttt) == len(vs):
                        break
                    vs = ttt
                vs = ttt
                #vs = vs.replace('  ',' ')

            #if len(ks) > max_ks_len:
                #ks = ks[:max_ks_len-3]+'...'

            vslines = vs.split('\n')
            if len(vslines) > 1:
                if len(vs) > max_vs_len:
                    vs = vs[:max_vs_len-3]+'...'

            left_side = '  ' + ' '*pad + ks + ' : '

            if len(vslines) > 1:
                left_pad = len(left_side) * ' '
                l2 = [vslines[0]]
                for lin in vslines[1:]:
                    lin = left_pad + lin
                    l2.append(lin)
                vs = '\n'.join(l2)

            s = left_side + vs
            l.append(s)
        s = '{\n' + '\n'.join(l) + '\n}'
        return s
