import socket
import time

def connect_to_proxy(proxy_host, proxy_port, local_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((proxy_host, proxy_port))
            print("[+] Подключено к прокси")

            # Здесь можно добавить перенаправление портов
            while True:
                data = s.recv(4096)
                if not data:
                    break
                # Отправляем данные на локальный RDP
                rdp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                rdp_socket.connect(("localhost", local_port))
                rdp_socket.send(data)
                response = rdp_socket.recv(4096)
                s.send(response)
                rdp_socket.close()
        except Exception as e:
            print(f"[-] Ошибка: {e}. Переподключение через 5 сек...")
            time.sleep(5)


if __name__ == "__main__":
    connect_to_proxy("your-proxy.onrender.com", 3391, 3390)