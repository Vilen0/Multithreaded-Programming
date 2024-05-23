#TCP сервер
# https://www.httpbin.org/



import socket
import sys

def get_html_content(url):
    # Разбираем URL
    if not (url.startswith("http://") or url.startswith("https://")):
        print("Только HTTP/HTTPS-ссылки поддерживаются.")
        return

    if url.startswith("http://"):
        url = url[7:]  # убираем "http://"
    else:
        url = url[8:]  # убираем "https://"

    host, path = url.split("/", 1)
    path = "/" + path

    # Создаем сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, 80))

    # Отправляем HTTP-запрос
    request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    client_socket.sendall(request.encode())

    # Получаем и выводим HTML-код страницы
    html_content = b""
    lines_printed = 0
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        html_content += data

        while b"\n" in html_content:
            index = html_content.index(b"\n")
            line = html_content[:index].decode()
            html_content = html_content[index + 1:]

            print(line)
            lines_printed += 1

            if lines_printed >= 25:
                input("Нажмите Enter для продолжения...")
                lines_printed = 0

    # Закрываем соединение
    client_socket.close()


if __name__ == "__main__":
    url = input("Введите URL: ")
    get_html_content(url)
