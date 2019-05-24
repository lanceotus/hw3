import os


class WebApplication:
    HTTP_Response_codes = {
        200: 'OK',
        404: 'NOT FOUND'
    }
    _DEFAULT_RESPONSE_CODE = 200
    _DEFAULT_CONTENT_TYPE = 'text/plain'
    _DOCS_DIR = './docs'

    def __init__(self):
        self.handlers = {}

    def __call__(self, environ, start_response):
        print(environ)

        resource = environ['PATH_INFO'].strip('/')
        print(resource)

        if resource in self.handlers:
            handler = self.handlers[resource]
        else:
            handler = self.er404_handler

        resp = handler(environ)
        resp_text = resp['text'] if 'text' in resp else ''
        resp_code = resp['code'] if 'code' in resp else self._DEFAULT_RESPONSE_CODE
        resp_content_type = resp['content_type'] if 'content_type' in resp else self._DEFAULT_CONTENT_TYPE
        status = '%s %s' % (resp_code, self.HTTP_Response_codes[resp_code])
        print(status)

        start_response(status, [('Content-Type', resp_content_type)])
        return [resp_text.encode('UTF-8')]

    def add_resource(self, resource, handler):
        self.handlers[resource] = handler

    @staticmethod
    def er404_handler(environ):
        doc_path = os.path.join(WebApplication._DOCS_DIR, '404.txt')
        if not os.path.exists(doc_path):
            return {'text': 'Object not found!', 'code': 404}

        resp = WebApplication.return_doc(environ, '404.txt')
        resp['code'] = 404
        return resp

    @staticmethod
    def return_doc(environ, docname):
        doc_path = os.path.join(WebApplication._DOCS_DIR, docname)
        if not os.path.exists(doc_path):
            return WebApplication.er404_handler(environ)

        with open(doc_path, encoding="UTF-8") as fp:
            content = fp.read()

        ext = docname.split('.')[-1]
        if ext == 'json':
            content_type = 'application/json'
        elif ext in ['htm', 'html']:
            content_type = 'text/html'
        else:
            content_type = 'text/plain'

        return {'text': content, 'content_type': content_type}

