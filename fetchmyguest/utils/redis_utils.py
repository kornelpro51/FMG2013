#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from redis import StrictRedis, ConnectionPool
from fetchmyguest import settings

pool = ConnectionPool(
    host=settings.SESSION_REDIS_HOST,
    port=settings.SESSION_REDIS_PORT,
    password=settings.SESSION_REDIS_PASSWORD,
    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
)


def get_redis_connection():
    return StrictRedis(host=settings.SESSION_REDIS_HOST,
                       port=settings.SESSION_REDIS_PORT,
#                       password=settings.SESSION_REDIS_PASSWORD,
#                       socket_timeout=settings.REDIS_SOCKET_TIMEOUT
    )