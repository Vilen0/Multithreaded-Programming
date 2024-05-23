#Кэширующий прокси

# curl -x localhost:8888 http://example.com
# curl -x localhost:8888 http://example2.com



import socket
import select
import threading
import time

class CacheProxy:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.cache = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Прокси запущен на {self.host}:{self.port}")

    def handle_client(self, client_socket):
        request = client_socket.recv(4096).decode()
        request_lines = request.split("\r\n")
        first_line = request_lines[0]
        url = first_line.split(" ")[1]

        if url in self.cache:
            print("Запрос находится в кэше")
            response = self.cache[url]
            #print("Кэш:", response)
        else:
            print("Запрос не найден в кэше. Отправляем запрос на сервер.")
            url_components = url.split("/")
            if len(url_components) < 3:
                print("Некорректный URL-адрес:", url)
                return
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((url_components[2], 80))
            server_socket.sendall(request.encode())
            response = server_socket.recv(4096)
            self.cache[url] = response
            #print("Кэш:", response)
            server_socket.close()

        client_socket.send(response)
        client_socket.close()

    def run(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            print("Получено новое соединение.")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    proxy = CacheProxy('localhost', 8888)
    proxy.run()
