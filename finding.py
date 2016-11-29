#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals


def findobjectpath( root, obj, depth=2 ):
    visited = set()
    #with nowarn():
    res = _findobjectpath( root, obj, depth, visited )
    return res




def _findobjectpath(node, obj, depth, visited):
    res = []
    visited.add(id(node))

    if depth <= 0: return res

    childrecs = []

    keys = dir( node )
    blackkeys = [
        '__dict__'
    ]
    for k in blackkeys:
        if k in keys:
            keys.remove(k)
    for k in keys:
        try:
            if hasattr(node, '__class__'):
                if hasattr(node.__class__, k):
                    cv = getattr(node.__class__, k)
                    if isinstance(cv, property):
                        continue
            v = getattr(node, k)
        except:
            continue
        childrecs.append(('.' + k,v))
        #if v is obj:
        #    res.append( '.' + k )

    if isdict(node):
        for k,v in node.iteritems():
            if v is obj:
                if isstring(k):
                    k_ = '["%s"]'%k
                else:
                    k_ = '[%s]'%str(k)
                childrecs.append((k_, v))
    elif islist(node) or istup(node) or isset(node):
        g = None
        try:
            g = enumerate(node)
        except: pass
        if g:
            for i,v in g:
                childrecs.append(( '[%d]'%i, v ))


    for k,v in childrecs:
        if v is obj:
            res.append(k)

        #breakon(k=='[3]')

        if id(v) not in visited:
            sub_res = _findobjectpath( v, obj, depth-1, visited )
        else:
            continue

        sub_res = [
            k +  s
            for s in sub_res
        ]
        #breakon(len(sub_res))

        res.extend( sub_res )


    return res


def isdict(v):
    return isinstance(v,dict)

def islist(v):
    return isinstance(v,list)

def istuple(v):
    return isinstance(v,tuple)

istup = istuple


def isset(v):
    return isinstance(v,set) # or isoset(v)

