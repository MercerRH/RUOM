from test_ import test_view


urls = [
    (r'^/test/(.*)$', test_view.test),
    (r'^/template/$', test_view.template_test),
]