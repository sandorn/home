# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : # #暂时无用，废弃
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-18 09:39:04
#FilePath     : /xjLib/xt_MetaClass.py
#LastEditTime : 2020-07-16 18:40:52
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import abc
import itertools

META_CLS = 0
HAS_META_CLS = 1
COMMON_CLS = 2


def is_metaclass(cls):
    return issubclass(cls, type)


def get_metaclass(cls):
    return cls if is_metaclass(cls) else type(cls)


def has_defined_metaclass(cls):
    return get_metaclass(cls) is not type


def _get_class_flag(cls):
    if is_metaclass(cls):
        return META_CLS
    if has_defined_metaclass(cls):
        return HAS_META_CLS
    else:
        return COMMON_CLS


def _get_three_kinds_of_classes(*mixins):
    all_mixins_group = itertools.groupby(mixins, _get_class_flag)

    mixin_metaclass_list = []
    mixin_has_metaclass_list = []
    mixin_common_list = []

    for mixin_group in all_mixins_group:
        if mixin_group[0] == META_CLS:
            mixin_metaclass_list = list(mixin_group[1])
        elif mixin_group[0] == HAS_META_CLS:
            mixin_has_metaclass_list = list(mixin_group[1])
        elif mixin_group[0] == COMMON_CLS:
            mixin_common_list = list(mixin_group[1])

    return mixin_metaclass_list, mixin_has_metaclass_list, mixin_common_list


def _get_meta_cls_and_original_class(cls):
    bases = cls.__bases__
    new_bases = []
    meta_cls = type(cls)

    for base in bases:
        if has_defined_metaclass(base):
            _, new_base = _get_meta_cls_and_original_class(base)
            new_bases.append(new_base)

        else:
            new_bases.append(base)
    return meta_cls, type(cls.__name__, tuple(new_bases), dict(cls.__dict__))


def _combined_metaclass(*metas):
    class CombinedMeta(*metas):
        pass

    return CombinedMeta


def generate_base(*mixins):
    mixin_metaclass_list, mixin_has_metaclass_list, mixin_common_list = _get_three_kinds_of_classes(*mixins)

    meta_and_common_list = [_get_meta_cls_and_original_class(mixin_has_metaclass) for mixin_has_metaclass in mixin_has_metaclass_list]

    for metacls, commoncls in meta_and_common_list:
        mixin_metaclass_list.append(metacls)
        mixin_common_list.append(commoncls)

    meta_cls = _combined_metaclass(*mixin_metaclass_list) if mixin_metaclass_list else type

    class BaseClass(metaclass=meta_cls, *mixin_common_list):
        @classmethod
        def get_metas(cls):
            mro = meta_cls.mro(meta_cls)

            def filter_name(name):
                filters = ['type', 'CombinedMeta', 'object']

                return not any((i in name for i in filters))

            metas = [m for m in mro if filter_name(m.__name__)]

            return metas

    return BaseClass
