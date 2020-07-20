from ..RUOM.views import append_to_url


@append_to_url('/test')
def test():
    return 'Hello world: test view_func'
