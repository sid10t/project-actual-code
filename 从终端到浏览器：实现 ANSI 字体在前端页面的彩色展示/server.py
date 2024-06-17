import http.server
import socketserver

import ansiconv


class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def check_client_address(self):
        # 设置白名单，只允许特定的IP地址或主机访问
        whitelist = ['127.0.0.1', 'localhost']  # 添加允许访问的IP地址或主机

        # 获取客户端的IP地址
        client_address = self.client_address[0]

        # 检查客户端IP地址是否在白名单中
        if client_address not in whitelist:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Forbidden. Please contact sidiot.')
            return False

        return True

    def read_file(self, content_type, file_io):
        try:
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.end_headers()
            self.wfile.write(file_io)

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'File not found!')

    def do_GET(self):
        if self.check_client_address():
            if self.path.startswith("/?plain="):
                file = open(self.path[8:], 'rb').read()
                plain = ansiconv.to_plain(file.decode('UTF-8'))
                self.read_file("text/plain", plain.encode())
            elif self.path.startswith("/?html="):
                file = open(self.path[7:], 'rb').read()
                conv = ansiconv.to_html(file.decode('UTF-8'))
                css = ansiconv.base_css()
                html = """
                <html>
                  <head><style>{0}</style></head>
                  <body>
                    <pre class="ansi_fore ansi_back">{1}</pre>
                  </body>
                </html>
                """.format(css, conv)
                print(html)
                self.read_file("text/html", html.encode())
            else:
                super().do_GET()


# 设置服务器的IP地址和端口号
host = '0.0.0.0'  # 监听所有网络接口
port = 8888

# 创建HTTP服务器并设置请求处理程序
with socketserver.TCPServer((host, port), HTTPRequestHandler) as httpd:
    httpd.serve_forever()
