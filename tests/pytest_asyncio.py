import asyncio
import pytest
import inspect


def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as asynchronous")


def pytest_pyfunc_call(pyfuncitem):
    if 'asyncio' in pyfuncitem.keywords:
        func = pyfuncitem.obj
        if inspect.iscoroutinefunction(func):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                kwargs = {
                    name: pyfuncitem.funcargs[name]
                    for name in pyfuncitem._fixtureinfo.argnames
                }
                loop.run_until_complete(func(**kwargs))
            finally:
                loop.close()
            return True
    return None
