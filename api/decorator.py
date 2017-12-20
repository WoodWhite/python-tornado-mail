# -*- coding: utf-8 -*-

import logging as log


def xxx_except(except_info):
    def decorator(func):
        def wrapper(self, *args, **kw):
            try:
                return func(self, *args, **kw)
            except Exception as e:
                log.error('[code: %d] %s body{%s} by [%s]' %
                          (except_info['Code'], except_info['Message'],
                           ''.join(self.request.body.split()), e))
                self.set_status(400)
                self.write(except_info)
        return wrapper
    return decorator


def xxx_auth(err_code):
    def decorator(func):
        def wrapper(self, *args, **kw):
            account = self.request.headers.get('Identifier', '')
            if not(isinstance(account, str) and account):
                self.code = err_code
                self.msg = 'Wrong Identifier!'
                self.set_status(401)
                self._response()
            else:
                func(self, *args, **kw)
        return wrapper
    return decorator
