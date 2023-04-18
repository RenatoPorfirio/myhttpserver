import socket as s

class HTTPServer:
  
  def __init__(self, ip, port):
    self.con_addr = (ip, port)
    with open('html/404.html', 'rb') as not_found:
      self.error_page = b'HTTP/1.1 404 NOT FOUND\n\n' + not_found.read()
    self.tcp = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.tcp.setsockopt(s.SOL_SOCKET, s.SO_KEEPALIVE, 1)
    self.tcp.bind(self.con_addr)
    self.tcp.listen(1)
    
  def serve_forever(self):
    print('Ouvindo na porta', self.con_addr[1], '...\nPressione Ctrl+C para encerrar.')
    try:
      while True:
        client_conn, client_addr = self.tcp.accept()
        request = client_conn.recv(1024).decode().split('\r\n')
        method, path, version = request[0].split()


#        if method == 'GET':
#          self.do_get()
#        elif method == 'POST':
#          self.do_post()
#        elif response = b'HTTP/1.1 codigo descrição\n\n'
        
        response = b''
        if path == '/':
          path += 'index'
        if path.split('.')[-1] == path:
          path += '.html'

        try:
          with open('html'+path, 'rb') as htm_file:
            response = b'HTTP/1.1 200 OK\n\n' + htm_file.read()
        except:
          response = self.error_page
        
        client_conn.sendall(response)
        print(client_addr[0], method, path, response.decode().split('\n')[0])
        client_conn.close()
    except:
      print('\nEncerrando serviço ...')
      client_conn.close()
      self.tcp.close()

  def do_get():
    pass

  def do_post():
    pass