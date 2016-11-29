#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

"""
todo:

reload: reloade das symbol im caller frame
"""


#from imp import reload
import importlib
import types


def add_to_globals(o, name=None):
    if name is None:
        n = getattr(o, '__name__')
    else:
        n = name

    # if isstring(n):
    assert isstring(n)
    globals()[n] = o


def myimport(k):
    es = k.split('.')
    name = k
    fromlist = ['.'.join(es[:-1])]
    mod = __import__(
        name=name,
        fromlist=fromlist,
    )
    return mod


def reload_objs_class(objs):
    #classes = set(V(objs).get('__class__'))
    class_seq = V(objs).get('__class__')
    o = reload_objs(class_seq)
    new_class_seq = o.newobjs
    for obj, newcls in V(objs) | new_class_seq:
        obj.__class__ = newcls
        # obj
    #newcls = reload_obj(cls)
    # for obj in objs:
        #obj.__class__ = newcls


def reload_obj_class(obj):
    if obj is None:
        return
    cls = obj.__class__
    newcls = reload_obj(cls)
    obj.__class__ = newcls

def reload_module(mod):
    import importlib
    newmod = importlib.reload(mod)
    return newmod

import sys

def reload_func(func):
    modname = func.__module__
    mod = sys.modules[modname]
    reload_module(mod)
    try:
        v = getattr(mod,func.__name__)
        return v
    except:
        pass

def reload_type(func):
    modname = func.__module__
    mod = sys.modules[modname]
    reload_module(mod)


def reload_any(o):
    if isinstance(o,types.ModuleType):
        return reload_module(o)
    elif isfunc(o):
        return reload_func(o)
    elif istype(o):
        return reload_type(o)
    else:
        print("not supported yet for this type")


def isfunc(o):
    return isinstance(o,types.FunctionType)

def istype(o):
    return isinstance(o,type)



class _roc:

    def __call__(self, o):
        reload_obj_class(o)

    def __truediv__(self, o):
        reload_obj_class(o)

roc = _roc()


def reload_objs(objs):
    l = V()
    for obj in objs:
        o = Obj()
        o.modstr = obj.__module__
        o.mod = myimport(o.modstr)
        o.name = obj.__name__
        o.oldobj = getattr(o.mod, o.name)
        l.append(o)
    recs = l

    mods = unique(recs.mod)
    modmap = OrderedDict()
    for mod in mods:
        print('MIC: reloading module', str(mod.__name__))
        m2 = importlib.reload(mod)

    l = V()
    for o in recs:
        newobj = getattr(o.mod, o.name)
        l.append(newobj)
    newobjs = l
    #print('NEW: ', str(newobj)+id_hex_str(newobj))
    # add_to_all_globals(newobj)

    o = Obj()
    o.newobjs = newobjs
    o.mods = mods

    return o


def reload_obj(obj):
    modstr = obj.__module__
    mod = myimport(modstr)
    name = obj.__name__
    oldobj = getattr(mod, name)
    print('OLD: ', str(oldobj) + id_hex_str(oldobj))
    importlib.reload(mod)
    newobj = getattr(mod, name)
    print('NEW: ', str(newobj) + id_hex_str(newobj))
    add_to_all_globals(newobj)
    return newobj


def id_hex_str(o):
    s = '_0x%x' % id(o)
    return s


def reload_class(cls, skipmodreload=False):
    reload_classes([cls], skipmodreload=skipmodreload)


def reload_classes(clss, skipmodreload=False):
    import gc

    objs = gc.get_objects()
    d = OrderedDict()
    for o in objs:
        c = getattr(o, '__class__', None)
        if c is not None:
            for cls in clss:
                k1 = (
                    c.__module__,
                    c.__name__,
                )
                k2 = (
                    cls.__module__,
                    cls.__name__,
                )
                if k1 == k2:
                    l = d.setdefault(cls, V())
                    l.append(o)

    if skipmodreload:
        newclss = V(clss)
    else:
        newclss = reload_objs(clss)

    #subobjs = V()
    # for cls in clss:
        #clss = get_subclasses_of_cls(cls)

    for cnew, cold in newclss | clss:
        if d.has_key(cold):
            l = d[cold]
            for o in l:
                if False:
                    assert o.__class__ is cold
                o.__class__ = cnew

    mods = get_my_loaded_modules()
    for cnew, cold in newclss | clss:
        kold = cold.__name__, cold.__module__
        nam = cold.__name__
        for mod in mods:
            modval = getattr(mod, nam, None)
            if modval is not None:
                knew = modval.__name__, modval.__module__
                if kold == knew:
                    setattr(mod, nam, cnew)
                    # mod

    o = Obj()
    o.oldclss = V(clss)
    o.newclss = newclss
    o.objs = V(objs)
    o.objmap = d

    #    __author__ = 'Michael Isik'
    #mods = V(sys.modules.values())
    # return mods

    return o


def get_my_loaded_modules():
    mods = get_all_loaded_modules()
    auths = mods.get('__author__', '')
    mods = mods[auths == 'Michael Isik']
    return mods


def get_all_loaded_modules():
    mods = V(sys.modules.values())
    return mods


def id_hex_str(o):
    s = '_0x%x' % id(o)
    return s


def add_to_all_globals(obj):
    name = obj.__name__

    import inspect
    for frame_tuple in inspect.stack():
        globs = frame_tuple[0].f_globals
        globs[name] = obj


def add_module_to_globals(mod):
    d = mod.__dict__
    ks = dir(mod)
    for k in ks:
        v = d[k]
        add_to_globals(v, name=k)
