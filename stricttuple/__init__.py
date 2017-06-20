#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: codykochmann
# @Date:     2017-04-06 13:35:45
# @Last Modified time: 2017-06-20 11:06:37

from collections import namedtuple
import inspect
import sys

class typedtuple(object):
    """ typedtuple is a namedtuple with type enforcement """

    _example_usage="""\n\nExample Usage:\n
    Point = typedtuple(
        'Point',
        x = int,
        y = int
    )\n"""
    _one_arg_needed="typedtuple needs one argument that will serve as the structname.{}".format(_example_usage)

    def __init__(self, *args, **kwargs):
        assert len(args) == 1, self._one_arg_needed
        self.validate_all_types(kwargs)
        self.fields=kwargs
        self.name=args[0]
        self.namedtuple=namedtuple(
            self.name,
            self.fields.keys()
        )

    @staticmethod
    def suggest_correct_type_defining(key, value):
        return

    @staticmethod
    def validate_all_types(kwargs):
        """ validates that all values of the arguments are types """
        for key in kwargs:
            assert isinstance(kwargs[key], type), """\n
    Typedtuple needs its arguments to be types. Argument "{k:}" was {type_name:}({val_repr}).
    You might want to try:
        {k:} = {type_name:}\n\n""".format(k=key, type_name=type(kwargs[key]).__name__, val_repr=kwargs[key].__repr__())

    def validate_fields(self, **kwargs):
        """ ensures that all incoming fields are the types that were specified """
        for field in self.fields:
            value = kwargs[field]
            required_type = self.fields[field]
            if type(value) != required_type:
                raise TypeError('{}.{} needs to be a {}, recieved: {}({})'.format(
                    self.name,
                    field,
                    required_type.__name__,
                    type(value).__name__,
                    value.__repr__()))

    def __call__(self, **kwargs):
        """ validates that the values match the specifications and
            returns a namedtuple with those fields and values """
        self.validate_fields(**kwargs)
        return self.namedtuple(**kwargs)

class stricttuple():
    @staticmethod
    def extract_types(*args):
        return (i for i in args if type(i) == type)

    @staticmethod
    def is_type(obj, *typ):
        assert len(typ) >= 1
        types = (i for i in typ if type(i) == type)
        return any((type(obj)==t) for t in types)

    def __init__(self, *args, **kwargs):
        args = args
        kwargs = kwargs
        self.namedtuple=namedtuple(
            args[0],
            kwargs.keys()
        )
        self.name=args[0]
        # validate the arguments coming in
        allowed_types = tuple, type
        assert len(args) == 1
        assert type(args[0]) == str
        assert all(type(v) in allowed_types for v in kwargs.values())

        lambda_type = type(lambda:1)
        allowed_types_in_tuples = type, lambda_type
        self.__saved_rules__={}
        for k in kwargs:
            v = kwargs[k]
            if type(v) == tuple:
                self.__saved_rules__[k]=[]
                for i in v:
                    assert type(i) in allowed_types_in_tuples
                    if type(i) == type:
                        self.__saved_rules__[k].append(lambda _:type(_)==i)
                    else:
                        self.__saved_rules__[k].append(i)
        #print(self.__saved_rules__)

    def __call__(self, **kwargs):
        """ validates that the values match the specifications and
            returns a namedtuple with those fields and values """
        for k in kwargs:
            v = kwargs[k]
            for r in self.__saved_rules__[k]:
                if not r(v):
                    exit('stricttuple rule violation\ninstruction:\n\t{}.{} = {}({})\nviolates the rule:\n\t{}'.format(
                        self.name,
                        k,
                        type(v).__name__,
                        repr(v),
                        inspect.getsource(r).strip()
                        ))
        return self.namedtuple(**kwargs)

if __name__ == '__main__':

    Point = typedtuple(
        'Point',
        x = int,
        y = int
    )

    t = Point(
        x = 3,
        y = 42
    )

    print(t)

    Point = stricttuple(
        "Point",
        x = (
             lambda x:type(x)==int,
             lambda x:x<15 and x>=0
        ),
        y = (
             lambda y:type(y)==int,
             lambda y:y<15 and y>=0
        )
    )

    from random import randint
    for i in range(32):
        t = Point(
            x=randint(0, 15),
            y=randint(0, 16)
        )
        print(t)
