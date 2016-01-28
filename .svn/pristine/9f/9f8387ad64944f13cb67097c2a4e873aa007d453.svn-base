# -*- mode: python; coding: utf-8 -*-
# Written by Sylvain Ferriol
# Commented by Dimitri Dubois

from twisted.internet import defer


def _call_func(func, obj, *args, **kw_args):
    """
    Return a defered placed on the function for the object. For this
    application the obj is a part which has the function as an attribute.
    """
    if type(func) is str:
        f = getattr(obj, func)
        d = defer.maybeDeferred(f, *args, **kw_args)
    else:
        d = defer.maybeDeferred(func, obj, *args, **kw_args)
    return d


@defer.inlineCallbacks
def forAll(objects, func, *args, **kw_args):
    """
    Create a list of defered: one deferred for each object.
    For this application objects are parts.
    """
    dl = []
    for obj in objects:
        # create of a deferred and put it in a list
        d = _call_func(func, obj, *args, **kw_args) 
        dl.append(d) 
    # yield means that we wait that all the deferred in the list have finished
    results = yield (defer.DeferredList(dl)) 
    ret = [res[1] for res in results]
    defer.returnValue(ret)


@defer.inlineCallbacks
def forEach(objects, func, *args, **kw_args):
    """
    create a deferred for each object
    Wait each one before to call the next one
    """
    for obj in objects: 
        yield (_call_func(func, obj, *args, **kw_args))



