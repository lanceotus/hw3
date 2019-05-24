from framework import WebApplication


def index_handler(environ):
    return WebApplication.return_doc(environ, 'index.html')


def catalog_handler(environ):
    return WebApplication.return_doc(environ, 'catalog.json')


application = WebApplication()
application.add_resource("", index_handler)
application.add_resource("catalog", catalog_handler)
