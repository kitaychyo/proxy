import socket
import threading


def handle_client(client_socket, target_host, target_port):
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))

    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        target_socket.send(data)

        response = target_socket.recv(4096)
        if not response:
            break
        client_socket.send(response)

    client_socket.close()
    target_socket.close()


def start_proxy(server_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', server_port))
    server.listen(5)
    print(f"[*] Прокси слушает порт {server_port} -> {target_host}:{target_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Подключение от {addr[0]}:{addr[1]}")
        proxy_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, target_host, target_port)
        )
        proxy_thread.start()


if __name__ == "__main__":
    # Настройки для RDP (перенаправляем 3390 -> ваш_пк:3389)
    start_proxy(server_port=3391, target_host="localhost", target_port=3390)