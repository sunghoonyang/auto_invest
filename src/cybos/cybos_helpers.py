"""
    DECORATOR COLLECTIONS
"""
from functools import wraps

__all__ = [
    'assert_cybos_connection',
]


def assert_cybos_connection(func):
    @wraps(func)
    def _impl(self, *func_args, **func_kwargs):
        import pywintypes
        try:
            assert self.instCpCybos.IsConnect == 1\
                , '**************\tConnection rejected. Run as admin, or connect to CybosPlus\t**************'
            return func(self, *func_args, **func_kwargs)
        except pywintypes.com_error as e:
            print('PyCharm is unable to call CpUtil.CpCybos DLL: %s' % str(e))
            raise
    return _impl