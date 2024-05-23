import socket

target_host = "127.0.0.1"
target_port = 27700

# Создаем сокетное соединение
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client.connect((target_host, target_port))

# Отправляем данные
client.send(b"SYN")  # Добавляем b перед строкой для отправки байтов

# Получаем ответ
response = client.recv(4096)

print(response.decode('utf-8'))  # Декодируем полученные байты в строку
