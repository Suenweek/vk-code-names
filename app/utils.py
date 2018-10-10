from contextlib import contextmanager

from .resource import Resource


resource = Resource()


@contextmanager
def ctx_if(cond, ctx_man):
    if cond:
        with ctx_man:
            yield
    else:
        yield