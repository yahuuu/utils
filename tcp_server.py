# coding:utf-8

from socket import *
import logging as logger
import concurrent.futures as futures

logger.basicConfig(level=logger.DEBUG)


class TCPServer:
    def __init__(self, host='', port=9000):
        self.HOST = host
        self.PORT = port
        self.BUFSIZ = 1024
        self.ADDRESS = (self.HOST, self.PORT)
        self.clients = []
        self.ex = futures.ThreadPoolExecutor(max_workers=3)

        self.tcpServerSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpServerSocket.bind(self.ADDRESS)
        logger.info("服务器启动，监听端口{}...".format(self.ADDRESS))
        self.tcpServerSocket.listen(5)

    def launch(self):
        while True:
            print('服务器正在运行，等待客户端连接...')
            client_socket, client_address = self.tcpServerSocket.accept()
            self.ex.submit(self.response, client_socket, client_address)
            print('客户端 {} 已连接！'.format(client_address))
            # self.clients.append((client_socket, client_address))
            self.clients = [(client_socket, client_address)]


    def response(self, client_socket, client_address):
        try:
            while True:
                data = client_socket.recv(self.BUFSIZ)
                if data:
                    print('接收到消息 {}({} bytes) 来自 {}'.format(data.decode('utf-8'), len(data), client_address))
                    for client in self.clients:
                        sock = client[0]
                        addr = client[1]
                        if sock != client_socket:
                            info = "{}:{}>>{}".format(addr[0], str(addr[1]), data.decode('utf-8'))
                            logger.info("向客户端{}：{}发送数据{}".format(addr[0], str(addr[1]), data.decode('utf-8')))

                            sock.send(info.encode('utf-8'))
                else:
                    print("客户端{}已断开！".format(client_address))
                    self.clients.remove((client_socket, client_address))
                    break
        finally:
            client_socket.close()


def main():
    ts = TCPServer()
    ts.launch()


main()
