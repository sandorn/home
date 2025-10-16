# d:/CODE/xjlib/xthttp/__init__.py
"""HTTP请求与响应处理模块"""

from __future__ import annotations

from .ahttp import AsyncHttpClient, ahttp_get, ahttp_get_all, ahttp_get_all_sequential, ahttp_post, ahttp_post_all
from .headers import TIMEOUT_AIOH, TIMEOUT_REQU, Head
from .requ import SessionClient, delete, get, head, options, patch, post, put
from .resp import HttpError, RespFactory, UnifiedResp

__version__ = '1.0.0'
__all__ = (
    'TIMEOUT_AIOH',
    'TIMEOUT_REQU',
    'AsyncHttpClient',
    'Head',
    'HttpError',
    'RespFactory',
    'SessionClient',
    'UnifiedResp',
    'ahttp_get',
    'ahttp_get_all',
    'ahttp_get_all_sequential',
    'ahttp_post',
    'ahttp_post_all',
    'delete',
    'get',
    'head',
    'options',
    'patch',
    'post',
    'put',
)
