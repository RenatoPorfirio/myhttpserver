import httpserver2 as http

httpd = http.HTTPServer('', 80)
httpd.serve_forever()