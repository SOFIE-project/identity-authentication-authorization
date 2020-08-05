from werkzeug.wrappers import Request, Response
from werkzeug.datastructures import Headers
import requests

class http_proxy:
    def forward(self, environ, target, header_rewrite = None):
        path    = environ.get('PATH_INFO')
        req     = Request(environ)
        accept  = req.headers.get('Accept')
        content = req.headers.get('Content-Type')
        headers = {}
        if(accept):
            headers['Accept'] = accept
        if(content):
            headers['Content-Type'] = content
        if(header_rewrite):
            headers.update(header_rewrite)
        if (req.method == "GET"):
            response  = requests.get(target + path, headers = headers)
        elif (req.method == "PUT"): 
            put_data = req.data
            response  = requests.put(target + path, headers = headers, data = put_data.decode())
        code = response.status_code
        output = response.text
        return code, output