import sys
import socket as s
import json

class HTTPServer:
  
  def __init__(self, ip, port):
    self.NOT_FOUND_HEADER = 'HTTP/1.1 404 NOT FOUND\n'
    self.NOT_IMPLEMENTED_HEADER = 'HTTP/1.1 501 NOT IMPLEMENTED\n'
    self.SUCESS_HEADER = 'HTTP/1.1 200 OK\n'
    self.ERROR_HEADER = 'HTTP/1.1 500 INTERNAL SERVER ERROR\n'
    self.NOT_ALLOWED_HEADER = 'HTTP/1.1 405 METHOD NOT ALLOWED\n'
    self.not_found_page = '\n<!DOCTYPE html><html><head><meta charset="utf-8"/><title>404</title></head><body><div class="text" style="margin: 0 auto; text-align: center;"><h1>PÁGINA NÃO ENCONTRADA!</h1><h2>VERIFIQUE O ENDEREÇO E TENTE NOVAMENTE.</h2></div></body></html>'
    self.index_page = '\n<!DOCTYPE html><html><head><meta charset="utf-8"/><title>index</title></head><body><h1>Bem vindo ao site da empresa RPELETRON,</h1><br><h2>especialista em vendas de artigos eletrônicos de todos os tipos!</h2></body></html>'
    self.srv_addr = (ip, port)
    self.tcp = s.socket(s.AF_INET, s.SOCK_STREAM)
    self.tcp.setsockopt(s.SOL_SOCKET, s.SO_KEEPALIVE, 1)
    self.tcp.bind(self.srv_addr)
    self.tcp.listen(1)
    
  def serve_forever(self):
    print('Ouvindo na porta', self.srv_addr[1], '...\nPressione Ctrl+C para encerrar.')
    try:
    #for i in range(0,1):
      while True:
        client_conn, client_addr = self.tcp.accept()
        request = client_conn.recv(1024).decode('utf-8').split('\r\n')
        method, path, version = request[0].split()
        response = ''
        #print(request)
        get_split = path.split('?')
        if path == '/':
          response += self.SUCESS_HEADER + '\n' + self.index_page
        elif get_split[0] == '/requests':
          if method == 'GET':
            try:
              response += self.do_get(get_split[1])
            except:
              response += self.ERROR_HEADER + '\n'
          elif method == 'POST':
            self.do_post()
          else:
            response += self.NOT_ALLOWED_HEADER + '\n'
        else:
          response += self.NOT_FOUND_HEADER + '\n' + self.not_found_page

        client_conn.sendall(response.encode('utf-8'))
        print(client_addr[0], 
              method,
              path,
              response.split('\n')[0])
        client_conn.close()
    except:
      print('\nEncerrando serviço ...')
      client_conn.close()
      self.tcp.close()

  def do_get(self, params):
    try:
      div = params.split('&')
      data = {}
      for atribute in div:
        name, value = atribute.split('=')
        data[name] = value
      return self.SUCESS_HEADER + 'Content-Type: application/json; charset=utf-8\n\nDEU CERTO!\n' + json.dumps(data, indent=3)
    except:
      return self.ERROR_HEADER + '\n'

  def do_post(self, jsn=None):
    return self.NOT_IMPLEMENTED_HEADER

def run(ip='', port=80):
  print('')
  try:
    httpd = HTTPServer(ip, port)
  except:
    print('Falha ao rodar o servidor com as configurações de linha de comando.')
    print('Iniciando com configuração padrão.\n')
    try:
      httpd = HTTPServer('', 5000)
    except:
      try:
        httpd = HTTPServer('', 8000)
      except:
        httpd = HTTPServer('', 8090)

  httpd.serve_forever()

try:
  run(sys.argv[1], int(sys.argv[2]))
except:
  run()