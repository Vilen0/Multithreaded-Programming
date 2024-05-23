import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 27700

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

# Это поток, который обрабатывает данные от клиента
def handle_client(client_socket):
    # Показываем данные от клиента
    request = client_socket.recv(1024)
    print("[*] Received: %s" % request.decode('utf-8'))  # Декодируем полученные байты в строку

    # Возвращаем пакет
    client_socket.send(b"ACK!")  # Отправляем байты

    client_socket.close()

while True:
    client, addr = server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

    # Активируем функцию для обработки данных от клиента
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
